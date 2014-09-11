from __future__ import division
from django.template.defaultfilters import register
import json
import array
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from .models import Debat, Escritori, Aportacio, Resum, Tema
from django.views.generic import ListView, UpdateView, DetailView
from .models import UserProfile, Vote, Votedebat, Link
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import AportacioForm, VoteForm, UserProfileForm, DebatForm, ResumForm, VotedebForm, LinkForm
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from datetime import datetime,time,date
import notification
from notification.models import Notice
from notification import models as notification
import django.dispatch
from tagging.models import TaggedItem, Tag
import pygraphviz as P
from collections import Counter
import nltk
from micawber.parsers import extract
from micawber.contrib.mcdjango.providers import bootstrap_basic
from django.utils import simplejson
from notification.views import NoticeUserFeed
# from notification.decorators import basic_auth_required, simple_basic_auth_callback
# from notification.feeds import NoticeUserFeed



class DebatListView(ListView):

    model = Debat
    # queryset = Debat.with_votes.all()
    # template_name = 'debat_list.html'
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        aportacio = get_object_or_404(Aportacio, pk=pk)
        return Debat.objects.filter(aportacio=aportacio, parent = None)

    def get_context_data(self, **kwargs):
        context = super(DebatListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Votedebat.objects.filter(voter=self.request.user)
            pk = self.kwargs['pk']
            aportacio = get_object_or_404(Aportacio, pk=pk)
            aux = Debat.objects.filter(aportacio=aportacio)
            debats_in_page = [debat.id for debat in aux]
            voted = voted.filter(debat_id__in=debats_in_page)
            voted = voted.values_list('debat_id', flat=True)
            context["voted"] = voted
            #recollim els usuaris que han votat la aportacio que genera el debat per a controlar posteriorment en l'html les votacions
            ap_voted_by = Vote.objects.filter(aportacio=aportacio)   #ap_voted_by = ("aportacions" voted by)
            ap_voted_by = ap_voted_by.filter(voter=self.request.user)
            ap_vots_total = ap_voted_by.count()
            ap_voted_by = ap_voted_by.values_list('aportacio_id', flat=True)
            context["ap_voted_by"] = ap_voted_by
            context["ap_vots_total"] = ap_vots_total
        return context
    # def get_context_data(self, **kwargs):
    #     context = super(DebatListView, self).get_context_data(**kwargs)
    #     pk = self.kwargs['pk']
    #     aportacio = get_object_or_404(Aportacio, pk=pk)
    #     context['aportacio'] = aportacio
    #         #filter(name__endswith = 'kease?')
    #     return context

class DebatDetailView(DetailView):
    model = Debat



# class FirstDebatCreateView(CreateView):
#     model = Debat
#     form_class = DebatForm
#
#
#     def form_valid(self, form):
#         pk = self.kwargs['pk']
#         debat = get_object_or_404(Debat, pk=id)
#         aportacio = get_object_or_404(Aportacio, pk=pk)
#         f = form.save(commit=False)
#         f.aportacio = aportacio
#         f.autor = self.request.user
#         f.save()
#
#
# #      codi seguent es per les notificacions        #}
#         users = User.objects.filter(username=aportacio.autor)
#         # notification.send_now(users, 'comment_to_app' )
#         autor = aportacio.autor
#         # debat_created = django.dispatch.Signal(providing_args=["autor", "size"])
#         notification.send([aportacio.autor], "comment_to_app", {"debat": debat})
# #codi seguent per enviar la notificacio a tots els membres del debat
#         debats = Debat.objects.filter(aportacio=aportacio)
#         userz = set()
#         for item in debats:
#             userz.add(item.autor)
#         # notification.send_now(userz, 'comment_to_com' )
#         for user in userz:
#             notification.send([user], "comment_to_com", {"debat": debat})
#
#
#
#
#         return super(FirstDebatCreateView, self).form_valid(form)

class DebatCreateView(CreateView):
    model = Debat
    form_class = DebatForm

    def get_initial(self):

        pk = self.kwargs['pk']
        id = self.kwargs['id']
        re = "Re:"
        if not id:
            aportacio = get_object_or_404(Aportacio, pk=pk)
            titol = re + aportacio.titol
            self.initial = {"titol":titol}
        else:
            debat = get_object_or_404(Debat, pk=id)
            titol = re + debat.titol
            self.initial = {"titol":titol}

        return self.initial

    def form_valid(self, form):
        pk = self.kwargs['pk']
        id = self.kwargs['id']
        debat = get_object_or_404(Debat, pk=id)
        aportacio = get_object_or_404(Aportacio, pk=pk)
        f = form.save(commit=False)
        if debat:
            f.parent = debat
        f.aportacio = aportacio
        f.autor = self.request.user
        f.save()
#      codi seguent es per les notificacions        #}
#         users = User.objects.filter(username=aportacio.autor)
        # notification.send_now(users, 'comment_to_app' )
        # autor = aportacio.autor
        # debat_created = django.dispatch.Signal(providing_args=["autor", "size"])
        # !!!!!!!!!!!!!!!!!!notification.send([aportacio.autor], "comment_to_app", {"debat": debat})
#codi seguent per enviar la notificacio a tots els membres del debat



        # debats = Debat.objects.filter(aportacio=aportacio)
        # userz = set()
        # for item in debats:
        #     userz.add(item.autor)
        # # notification.send_now(userz, 'comment_to_com' )
        # for user in userz:
        #     notification.send([user], "comment_to_com", {"debat": debat})


        return super(DebatCreateView, self).form_valid(form)


class DebatUpdateView(UpdateView):
    model = Debat
    form_class = DebatForm


class DebatDeleteView(DeleteView):
    model = Debat
    success_url = reverse_lazy("escritori")

# Create your views here.
class EscritoriListView(ListView):
    model = Escritori
    queryset = Escritori.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EscritoriListView, self).get_context_data(**kwargs)
        context['escritoris'] = Escritori.objects.all()    #filter(name__endswith = 'kease?')
        return context

class AportacioListView(ListView):
    model = Aportacio
    queryset = Aportacio.with_votes.all()
    paginate_by = 5
    # def get_context_data(self, **kwargs):
    #     context = super(AportacioListView, self).get_context_data(**kwargs)
    #     context['aportacions'] = Aportacio.objects.all()    #filter(name__endswith = 'kease?')
    #     return context

    def get_context_data(self, **kwargs):
        context = super(AportacioListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            aportacions_in_page = [aportacio.id for aportacio in context["object_list"]]
            voted = voted.filter(aportacio_id__in=aportacions_in_page)
            voted = voted.values_list('aportacio_id', flat=True)
            context["voted"] = voted
        return context


class AportacioxTemaListView(ListView):
    model = Aportacio
    paginate_by = 5

    def get_queryset(self):
            pk = self.kwargs['pk']
            tema = get_object_or_404(Tema, pk=pk)
            return  Aportacio.with_votes.filter(tema=tema).all()

    def get_context_data(self, **kwargs):
        context = super(AportacioxTemaListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            aportacions_in_page = [aportacio.id for aportacio in context["object_list"]]
            voted = voted.filter(aportacio_id__in=aportacions_in_page)
            voted = voted.values_list('aportacio_id', flat=True)
            context["voted"] = voted
        return context

class AportacioxTagListView(ListView):
    model = Aportacio
    paginate_by = 5

    def get_queryset(self):
            slug = self.kwargs['slug']
            tag = get_object_or_404(Tag, name=slug)
            return TaggedItem.objects.get_by_model(Aportacio,tag)


    def get_context_data(self, **kwargs):
        context = super(AportacioxTagListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            aportacions_in_page = [aportacio.id for aportacio in context["object_list"]]
            voted = voted.filter(aportacio_id__in=aportacions_in_page)
            voted = voted.values_list('aportacio_id', flat=True)
            context["voted"] = voted
        return context

class AportacioDetailView(DetailView):
    model = Aportacio

    def get_context_data(self, **kwargs):
        context = super(AportacioDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        aportacio = get_object_or_404(Aportacio, pk=pk)
        items_related = TaggedItem.objects.get_related(aportacio, Aportacio)
        context["items_related"] = items_related

        return context

#############################################3 summarizer del text per a posar el resum en l'entradilla
##//////////////////////////////////////////////////////
##  Simple Summarizer
##//////////////////////////////////////////////////////
# Simple Summarizer
# Copyright (C) 2010-2012 Tristan Havelick
# Author: Tristan Havelick <tristan@havelick.com>
# URL: <https://github.com/thavelick/summarize/>
# For license information, see LICENSE.TXT
###https://github.com/thavelick/summarize/


from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer


class SimpleSummarizer:

	def reorder_sentences( self, output_sentences, input ):
		output_sentences.sort( lambda s1, s2:
			input.find(s1) - input.find(s2) )
		return output_sentences

	def get_summarized(self, input, num_sentences ):
		# TODO: allow the caller to specify the tokenizer they want
		# TODO: allow the user to specify the sentence tokenizer they want

		tokenizer = RegexpTokenizer('\w+')

		# get the frequency of each word in the input
		base_words = [word.lower()
			for word in tokenizer.tokenize(input)]
		words = [word for word in base_words if word not in SPANISH_STOPWORDS]
		word_frequencies = FreqDist(words)

		# now create a set of the most frequent words
		most_frequent_words = [pair[0] for pair in
			word_frequencies.items()[:100]]

		# break the input up into sentences.  working_sentences is used
		# for the analysis, but actual_sentences is used in the results
		# so capitalization will be correct.

		sent_detector = nltk.data.load('tokenizers/punkt/spanish.pickle')
		actual_sentences = sent_detector.tokenize(input)
		working_sentences = [sentence.lower()
			for sentence in actual_sentences]

		# iterate over the most frequent words, and add the first sentence
		# that inclues each word to the result.
		output_sentences = []

		for word in most_frequent_words:
			for i in range(0, len(working_sentences)):
				if (word in working_sentences[i]
				  and actual_sentences[i] not in output_sentences):
					output_sentences.append(actual_sentences[i])
					break
				if len(output_sentences) >= num_sentences: break
			if len(output_sentences) >= num_sentences: break

		# sort the output sentences back to their original order
		return self.reorder_sentences(output_sentences, input)

	def summarize(self, input, num_sentences):
		return " ".join(self.get_summarized(input, num_sentences))



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++HASHTAGIFY


#http://blog.swayy.co/post/61672584784/an-algorithm-for-generating-automatic-hashtags





# This is a simple tool for adding automatic hashtags into an article title
# Created by Shlomi Babluki
# Sep, 2013


SPANISH_STOPWORDS = set(nltk.corpus.stopwords.words('spanish'))


class Hashtagify(object):

    def __init__(self, title, content):
        self.index = Counter()
        self.title = self.add_sentence_to_index(title, True)
        self.build_index(content)

    # ** Helper function for building the index
    # Stem a single token
    def stem(self, token):
        sb = nltk.stem.snowball.SpanishStemmer()
        return sb.stem(token)

    # ** Helper function for building the index
    # Split a sentence into a list of tokens
    def tokenize_sentence(self, sentence):
        # sent_detector = nltk.data.load('tokenizers/punkt/spanish.pickle')
        # tokens = sent_detector.word_tokenize(sentence)
        tokens = nltk.word_tokenize(sentence)
        return tokens



    # ** Helper function for building the index
    # Add a single sentence into the index
    def add_sentence_to_index(self, sentence, is_title=False):
        tokens_list = []
        unstem_dic = {}
        prev_token = None

        # Split the sentence into tokens
        tokens = self.tokenize_sentence(sentence)
        for t in tokens:

            # Ignore stopwords
            if self.stem(t) in SPANISH_STOPWORDS:
                prev_token = None
                continue

            # Ignore words with one character (probably punctuations)
            if len(self.stem(t)) < 3:
                prev_token = None
                continue

            # *** Update the index ***

            # Unigram
            self.index[self.stem(t)] += 1

            # Bigram
            if prev_token:
                self.index["%s %s" % (prev_token, self.stem(t))] += 1
            prev_token = self.stem(t)

            tokens_list.append(self.stem(t))
            unstem_dic[self.stem(t)] = t
        return (sentence, tokens_list, unstem_dic)

    # Building the index
    def build_index(self, text):

        # Some pre-processing
        # text = text.decode('utf8')
        text = text.replace(u"\u2019", "'")
        text = text.replace(u"\u2014", "-")
        text = text.replace(u"\u201c", "\"")
        text = text.replace(u"\u201d", "\"")
        text = text.replace("\n", " ")

        # Split the text into sentences
        sent_detector = nltk.data.load('tokenizers/punkt/spanish.pickle')
        sentences = sent_detector.tokenize(text)

        # sentences = nltk.sent_tokenize(text)

        # Add each sentence into the index
        for sentence in sentences:
            self.add_sentence_to_index(sentence.strip())

    # Special case for merging two hashtags
    # Ex. (#Social #Media) --> (#SocialMedia)
    def merge_words(self, t1, t2):
        t1 = t1.replace("#", "")
        t2 = t2.replace("#", "")
        merge = "%s %s" % (self.stem(t1), self.stem(t2))

        if self.index[merge] / self.index[self.stem(t1)] < 0.5:
            return None

        if self.index[merge] / self.index[self.stem(t2)] < 0.5:
            return None

        return "#%s%s" % (t1, t2)

    # Add hashtags to the title
    def hashtagify(self, ratio):

        # Calculate how many words to convert
        total = int(len(self.title[1]) * ratio)

        # Rank the words in the title according to the index
        ranks = []
        for t in self.title[1]:
            ranks.append((t, self.index[t]))
        sorted_ranks = sorted(
            ranks,
            key=lambda k: k[1],
            reverse=True
        )

        # Convert the most common words into hashtags
        # for token in sorted_ranks[:total]:
        #     self.title[2][token[0]] = "#%s" % self.title[2][token[0]]

        # Rebuild the title. Merge hashtags if necessary.
        prev_tag = None
        hashtagify_title = []
        for t in self.title[1][:total]:
            word = self.title[2][t]
            if word.startswith("#"):
                if prev_tag:
                    merged_tag = self.merge_words(prev_tag, word)
                    if merged_tag:
                        hashtagify_title.pop()
                        hashtagify_title.append(merged_tag)
                    else:
                        hashtagify_title.append(word)
                else:
                    hashtagify_title.append(word)
                prev_tag = word
            else:
                hashtagify_title.append(word)
                prev_tag = None

        return " ".join(hashtagify_title).replace(" , ", ", ").strip()

#+++++++++++++++++++++++HASHTAGIFY+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++end













class AportacioCreateView(CreateView):
    model = Aportacio
    form_class = AportacioForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.autor = get_object_or_404(User, pk=self.request.user.pk)

# Python code for segmentation, POS tagging and tokenization

        # rawtext = open(f.entradilla).read
        # sentences = nltk.sent_tokenize("They have eaten dogs cat. In the garden of love") # NLTK default sentence segmenter
        # sentences = [nltk.word_tokenize(sent) for sent in sentences] # NLTK word tokenizer
        # sentences = [nltk.pos_tag(sent) for sent in sentences] # NLTK POS tagger
        # pattern = "NP: {<DT>?<JJ>*<NN>}"
        # NPChunker = nltk.RegexpParser(pattern)
        # for sent in sentences:
        #     result = NPChunker.parse(sent)
        # text=f.entradilla


        s = f.titol
        c = f.text
        ht = Hashtagify(c, c)
        hashtagify_title = ht.hashtagify(0.008)
        s = hashtagify_title
        d = f.tags
        f.tags = d + s



#inici del codi per a summaritzar el text entrat en l entradilla

        ss=SimpleSummarizer()
        if not f.entradilla:
            f.entradilla=ss.summarize(f.text, 3)
##fi del codi per summaritzar el text en l'entradeta

# #inici del codi per a llistar els enllacos que hi hagi en el text
#         p = bootstrap_basic()
#         links = extract(f.text,p)
#         for link in links:
#             s = Link.objects.get_or_create(url=link)
#             f.links
#
# #fi del codi per llistar enllacos
        f.save()
        return super(AportacioCreateView, self).form_valid(form)


class AportacioUpdateView(UpdateView):
    model = Aportacio
    form_class = AportacioForm
    template_name = "Xarxa/aportacio_updateform.html"


class AportacioDeleteView(DeleteView):
    model = Aportacio
    success_url = reverse_lazy("escritori")


class ResumListView(ListView):
    model = Resum
    queryset = Resum.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ResumListView, self).get_context_data(**kwargs)
        tags = Tag.objects.usage_for_model(Aportacio, counts=True)
        for tag in tags:
            aportacions = TaggedItem.objects.get_by_model(Aportacio, tag)
            for aportacio in aportacions:
                tag.count=tag.count+tag.count*aportacio.rank_score
        tags = sorted(tags, key=lambda x: x.count, reverse=True )
        context['tags'] = tags    #filter(name__endswith = 'kease?')
        return context

class ResumxTemaListView(ListView):
    model = Resum
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(ResumxTemaListView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        tema = get_object_or_404(Tema, pk=pk)
        tags = Tag.objects.usage_for_queryset(Aportacio.objects.filter(tema=tema), counts=True)
        for tag in tags:
            aportacions = TaggedItem.objects.get_by_model(Aportacio, tag)
            for aportacio in aportacions:
                tag.count=tag.count+tag.count*aportacio.rank_score
        tags = sorted(tags, key=lambda x: x.count, reverse=True )
        context['tags'] = tags #filter(name__endswith = 'kease?')
        context['tema_pk'] = pk
        return context

class ResumDetailView(DetailView):
    model = Resum


class ResumCreateView(CreateView):
    model = Resum
    form_class = ResumForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.save()
        return super(ResumCreateView, self).form_valid(form)

class ResumUpdateView(UpdateView):
    model = Resum
    form_class = ResumForm


class ResumDeleteView(DeleteView):
    model = Resum
    success_url = reverse_lazy("escritori")



class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})

class UserProfileDeleteView(DeleteView):
        model = get_user_model()
        success_url = reverse_lazy("escritori")
        slug_field = "username"
    # def get_object(self, queryset=None):
    #     user = super(UserProfileDeleteView, self).get_object(queryset)
    #     UserProfile.objects.get_or_create(user=user)
    #     return user

class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response





class VoteFormBaseView(FormView):
    form_class = VoteForm


    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        aportacio = get_object_or_404(Aportacio, pk=form.data["aportacio"])
        user = self.request.user
        prev_votes = Vote.objects.filter(voter=user, aportacio=aportacio)
        has_voted = (len(prev_votes) > 0)

        ret = {"success": 1}
        if not has_voted:
            # add vote
            v = Vote.objects.create(voter=user, aportacio=aportacio)
            ret["voteobj"] = v.id
        else:
            # delete vote
            prev_votes[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)

class VoteFormView(JSONFormMixin, VoteFormBaseView):
    pass

#fins aqui era la part de codi per a votar aportacions, a partir d'aqui ve el codi per votar debats

class JSON2FormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response


class VotedebatFormBaseView(FormView):
    form_class = VotedebForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        debat = get_object_or_404(Debat, pk=form.data["debat"])
        user = self.request.user
        prev_votes = Votedebat.objects.filter(voter=user, debat=debat)
        has_voted = (len(prev_votes) > 0)

        ret = {"success": 1}
        if not has_voted:
            # add vote
            v = Votedebat.objects.create(voter=user, debat=debat)
            ret["votedebatobj"] = v.id
        else:
            # delete vote
            prev_votes[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)

class VotedebatFormView(JSON2FormMixin, VotedebatFormBaseView):
    pass




def pygraphviz_graph(request, pk):


    A=P.AGraph() # init empty graph
    # set some default node attributes
    A.graph_attr.update(size="300,300")
    A.node_attr['style']='filled'
    # A.node_attr['shape']='circle'

    if pk <> '0':
        aportacions=Aportacio.objects.filter(tema=pk)
        tags = Tag.objects.usage_for_queryset(aportacions, counts=True)
    else:
        tags = Tag.objects.all()


    for tag in tags:
        tagzs = Tag.objects.related_for_model(tag, Aportacio, counts=True, min_count=None)
        for tagz in tagzs:
    # Add edges (and nodes)
            A.add_edge(tag.name, tagz.name, label=tagz.count, penwidth=tagz.count)
            # if tagz.count>0:
            #     edge = A.get_edge(tag.name, tagz.name)
            #     edge.attr['weight']=5
    A.layout() # layout with default (neato)
    png=A.draw(format='png' ) # draw png
    return HttpResponse(png, mimetype='image/png')
#
# if __name__ == '__main__':
#     print ""






# @register.inclusion_tag('base.html')
# def show_num_notif():
#     notifs=4
#     # notifs = Notice.objects.filter(is_unseen=True).count
#     return { 'notifs' : notifs }


from micawber.parsers import extract
from micawber.contrib.mcdjango.providers import bootstrap_basic
# from flask import Flask, request
#
# app = Flask(__name__)

# @app.route('/links', methods=['POST'])

# def links(request):
# #inici del codi per a llistar els enllacos que hi hagi en el text
#      if request.is_ajax():
#         p = bootstrap_basic()
#         text = request.post.get['text', None]
#         if text:
#             links = extract(text,p)
#             # to_json = {
#             #     "item": text
#             # }
#         # response_dict = {}
#
#
#         # for link in links[0]:
#         # message = "Yes Ajax"
#             # response_dict.update({'link': link })
#             # l = list.append(link)
#         return HttpResponse(text)
        # return HttpResponse(json.dumps(to_json), mimetype='application/json')
            # s = Link.objects.get_or_create(url=link)
            # instance.links.add(s[0])

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import httplib

from urlparse import urlparse

def split_url(url):
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path

def verify_url(domain, path):
        try:
            conn = httplib.HTTPConnection(domain)
            conn.request('HEAD', path)
            response = conn.getresponse()
            conn.close()
        except:
            return False


def link_verify(request):


    # linkv=[]
        # array.array('i')
    linkv={}
    links = request.POST.getlist('links[]')
    # validate = URLValidator()
    # linkv.append("http://www.google.es")
    # linkv.append("http://www.youtube.com")
    i=0
    for link in links:
        url = link
        domain, path = split_url(url)
        if(verify_url(domain, path) is not False):
                if(i<4):
                    linkv[i]=link
                    i=i+1
    return HttpResponse(json.dumps(linkv), content_type='application/json')

class JSON3FormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response




class LinkFormBaseView(FormView):
    form_class = LinkForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        text = form.data["url"]
        has_text = (len(text) > 0)
        ret = {"success": 1}
        if has_text:
                    v = Link.objects.create(url=text)
                    ret["voteobj"] = v.id
                    return self.create_response(ret, True)
        # else:
        #     return 0


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)

class LinkFormView(JSON3FormMixin, LinkFormBaseView):
    pass