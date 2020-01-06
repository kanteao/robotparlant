# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*
# coding: utf-8
###############################################################################
# PyDial: Multi-domain Statistical Spoken Dialogue System Software
###############################################################################
#
# Copyright 2015 - 2018
# Cambridge University Engineering Department Dialogue Systems Group
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

"""
RegexSemI_TV.py - regular expression based TV SemI decoder
=====================================================================


HELPFUL: http://regexr.com

"""

'''
    Modifications History
    ===============================
    Date        Author  Description
    ===============================
    Jul 21 2016 lmr46   Refactoring, creating abstract class SemI
'''

import RegexSemI
import re,os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
from utils import ContextLogger
logger = ContextLogger.getLogger('')


class RegexSemI_KUSTOM(RegexSemI.RegexSemI):
    """
    """
    def __init__(self, repoIn=None):
        RegexSemI.RegexSemI.__init__(self)  #better than super() here - wont need to be changed for other domains
        self.domainTag = "KUSTOM"  #FIXME
        self.create_domain_dependent_regex()

    def init_regular_expressions(self):
        self.rHELLO = ur"^\s*(?:s(?:lt|alut?)|b(?:on|'|)j(?:ou)?r?|coucous?|cc|wesh|yo)\s"
        self.rNEG =  ur"^\s*(?:n(?:an|o(?:n|pe))\b|pas?\s*(?:di[est]?\s*)[cç]a|incorr?ecte?|(?:il\s*y'?\s*[aà]\s*erreur)|pas\s*(?:corr?ecte?|[cç](?:el)?a|bons?|(?:biens?\s*compri[est]?)))\s"
        self.rAFFIRM = ur"^\s*(?:oua?is?|ye[ps]|ok|[cçs]a\s*m['e]?\s*va[st]?|absolue?ment|(?:c(?:e\s*n|)'?\s*e(?:ts?|st?)\s*|)(?:bons?|corr?ecte?|[cçs]a))\s*$"
        self.THATSALL = ur"c(?:'?e(?:st?|ts?)|e\s*serr?as?)\s*tou[ts](?:\s*pour\s*(?:moi|nous)|)"
        self.GREAT = ur"nickele?|nice|g[eé]niale?|pas?\s*male?|(?:tr(?:[eéè]s|op?)\s*)biens?"
        self.HELPFUL = ur"(?:c'?\s*(?:[eé]tai[st]?|e(?:st?|ts?))\s*|)(?:une?\s*info(?:rmations?)\s*|)(?:ass(?:ez|[eé]e?)\s*|)utiles?"
        self.THANK = ur"thx|[cs]imer(?:\s*bro|h?omer|albert?)|mer[csk]i\s*(?:b(?:eau|o|)c(?:ou|)p|)"
        self.BYE = ur"au\s*re?v(?:oi?|i?o)r[ers]?|[+a]\+\s*(?:dans\s*l['e]?\s*bus|)"
        self.rBYE = (
            ur"^\s*(?:" +
                ur"(?P<GREAT1>" + self.GREAT + ur"\s*(?:[,\.!]\s*|)|)" + ur"(?P<HELPFUL1>" + self.HELPFUL + ur"\s*(?:[,\.!]\s*|)|)" +
                ur"|(?P<THATSALL>" + self.THATSALL + ur"\s*([,\.!]\s*|))" +
            ur")(?:" +
                ur"(?P<THANK1>" + self.THANK + ur"\s*(?:,\s*|et\s*|))" + ur"(?P<BYE1>" + self.BYE + ur"\s*|)" +
                ur"|(?P<BYE2>" + self.BYE + ur")\s*" + ur"(?P<THANK2>(?:[,\.!]\s*|et\s*|)" + self.THANK + ur"\s*|)" +
            ur")(?:[\.!]\s*|)$"
        )
        self.rTHANKS = (
            ur"^\s*(?P<GREAT>" + self.GREAT + ur"\s*(,\s*)|)(?:" +
                ur"(?P<HELPFUL>" + self.HELPFUL + ur"\s*(,\s*)|)(?P<THANK>" + self.THANK + ur")" +
                ur"|(?P<THANK>" + self.THANK + ur"\s*(,\s*)|)(?P<HELPFUL>" + self.HELPFUL + ur")" +
            ur")(?:[\.!]\s*|)$"
        )
        self.rREQALTS = (
            # heading part : [isthere|iwant|canihave|mayihave]
            ur"^\s*(?:" +
                ur"(?:j[e']?\s*|on|nous)\s*" +
                ur"(?:en\s*)?" +
                ur"(?:" +
                    ur"v(?:oudr(?:ai[estx]|i?on[st])|eu[stx])" +
                    ur"|pr[eé]f[eè]re(?:rai[est]|s|)\s*" +
                    ur"|aimerai[est]|peu[stx]?\s*avoir" +
                    ur"|" +
                ur")\s*" +
                ur"|y'?\s*a-?\s*t-?\s*ils?\s*" +
                ur"|p(?:uis|eu[stx]|ourrai[est])-?\s*(?:je|on)\s*avoir\s*" +
            ur"|)" +
            # Central part : <(an)other|alternative>
            ur"(?:" +
                ur"(?:(?:une?(?:\s*(?:choses?|trucs?|machins?|options?|propositions?))?|quell?e?\s*que\s*chose\s*d[e']?|choses?|trucs?|machins?|options?|propositions?|choi[esx]|d'?)\s*|)" +
                ur"(autres?|diff[eé]rente?s?|alternati[fv]e?s?)" +
                ur"(?:\s*(?:choses?|trucs?|machins?|options?|propositions?|choi[esx])|)" +
            ur")" +
            # if available
            ur"(?:si\s*(?:vous\s*avez(?:\s*[cç]e?l?a|)|t[u']?\s*as?(?:\s*[cç]e?l?a|)|(?:(?:c(?:'|ela)\s*est\s*|)possible))|)" +
            # Tail : courtesy
            ur"(?:\s*s'?\s*(?:il\s*|)(?:te?|v(?:ous|))\s*p(?:la[iî][st]|)|)" +
            # Quesiton mark for correctness
            ur"\s*(?:\?\s*|)$" +

            # idontwantthis
            ur"|^\s*(?:j(?:e\s*n'?\s*en?|'?\s*en)\s*|on\s*(?:n['e]?\s*|)|)" +
            ur"veu[stx]\s*pas" +
            ur"(?:\s*(?:d['e]\s*|)[cç](?:e?l?a|elui-?\s*(?:ci|l[aà])|et?t?e?s?\s*(?:choses?|trucs?|machins?|options?|propositions?|choi[esx]))|)\s*(?:!\s*|)$"
        )
        self.rREPEAT = (
            ur"^\s*(?:(?:tu\s*|)peu[stx]?\s*(?:-\s*tu\s*|)|(?:vous\s*|)pouvez\s*(?:-\s*vous\s*|)|)" +
            ur"(r(?:[eé]p[eéè]te[rsz]?|edi[str]?e?s?))" +
            ur"(?:\s*[cç]e?l?a|)" +
            # Tail : courtesy
            ur"(?:\s*s'?\s*(?:il\s*|)(?:te?|v(?:ous|))\s*p(?:la[iî][st]|)|)" +
            # Quesiton mark for correctness
            ur"\s*(?:\?\s*|)$"
        )
        # The remaining regex are for the slot,value dependent acts - and so here in the base class are \
        # just aiming to catch intent.
        # REQUESTS:
        self.WHATIS = ur"(?:(?:quell?e?\s*(?:est|sont)\s*)?l[ea]|combien\s*(?:y'?\s*)?a-?\s*t-\s*il\sde|s(?:['i]?\s*il|i)\s*(?:y'?\s*)?a(?:\s*d[eu]s?\b)?)"
        self.IT = ur"l[ae]s?"
        self.CYTM = ur"(?:(?:(?:tu\s*)?peu[stx]?\s*(?:-\s*tu\s*)?)?me\s*dire|di[st]\s*moi)"
        self.NEGATE =ur"((i\ )*(don\'?t|do\ not|does\ not|does\'?nt)\ (care|mind|matter)(\ (about|what))*(\ (the|it\'?s*))*)"
        self.DONTCARE = (ur"()(?:(?:(?:je\s*)?m|(?:on\s*)?s)'?en?\s*(?:f(?:iche|ou[st])|tape|cogne|branle|bat\s*les\s*couilles)\s*(?:d[ue]s?)?" +
            ur"|(?:c'?e(?:st?|ts?)\s*)?pas?\s*graves?" +
            ur"|[cç]a\s*importe\s*p(?:as?|eu)" +
            ur"|peu[stx]?\s*importe(?:\s*l[ae]s?)?" +
            ur"|(?:j'?\s*en\s*ai\s*)?rien\s*[aà]\s*(?:f(?:out|ai)re|battre|cir[eé]r?)(?:\s*de\s*[cç]a)?" +
            ur"|ba(?:llec|t\s*les\s*couilles|lais?\s*couilles?)(?:\s*fr[eè]re?)?" +
        ")")
        self.DONTCAREWHAT = "(i\ dont\ care\ what\ )"
        self.DONTCAREABOUT = "(i\ dont\ care\ about\ )"
        self.rREQUEST = ur"(\b|^|\s)("+self.CYTM+r"\s*("+self.WHATIS+r"|"+self.IT+r"))"
        # INFORMS:
        self.WANT = ur"(?:pourquoi\s*pas?|(?:j[e']|on)\s*v(?:eu[stx]|oudron[st])(?:\s*qu'?il\s*y\s*(?:aie?t?s?|est?|ets?))?|avec|j'ai\s*besoin\s*d[e']|(?:je\s*)(?:re)?cherche|(?:je\s*suis?\s*)habitue\s*a)(?:\s*(?:une?|des?|du))?"
        self.WBG = ur"(?:(?:serr?ai[est]\s*"+self.GREAT+ur")(?:$|[^\?]$))"
        self.rINFORM = ur"(?:\b|^|\ )"+self.WANT
        self.rINFORM_DONTCARE = self.DONTCARE+ur"\s*(?:comment|[aà]\s*quell?e?\s*point?|si)\s*c'?e(?:st?|ts?)"
        self.rINFORM_DONTWANT = ur"(?:je\s*[nl]e\s*veu[estx]\s*pas?(?:\s*que\s*[cç][ae]\s*so[iy][est]s?))"
        # Contextual dontcares: i.e things that should be labelled inform(=dontcare)
        self.rCONTEXTUAL_DONTCARE = self.DONTCARE
        # The following are NOT regular expresions, but EXACT string matching:
        self.COMMON_CONTEXTUAL_DONTCARES = [ur"(?:n'?|peu[st]?)\s*(importe)(?:\s*quoi)?", self.DONTCARE]
        self.COMMON_CONTEXTUAL_DONTCARES += ["it doesn\'t matter", "dont care"]


        self.general_INFORM = ur"(?:(?:j[e']|on)\s*(?:(?:v(?:eu|oudrai)[stx]?|pr[eé]f[eè]re(?:rai[stx]?|s|)|(?:aime(?:rai[stx]?|s|)))\s*(?:biens?|)|(?:ai|aurai[stx]?)\s*(?:biens?|)\s*(?:besoin|envie)(?:\s*d[e'])?)\s*(?:que\s*[cç]e?l?[ae]\s*so(?:i[stx]?|yen?t?s?)|quel(?:les?\s*)?que\s*chose\s*d['e]|une?\s*(?:truc|machin)s?|))"
        self.contextual_NOT = ur"(?:n(?:o(?:n|pe)|an)|(?:absolument|surtout|certainement)\s*pas?|pas?\s*du\s*tou[stx]?)"
        self.contextual_YES = ur"(?:oua?is?|ye[ps]|tou[stx]\s*[aà]\s*fai[st](?:\s*le\s*f(?:ai|eu?)san[st])?|absolument)"
        self.contextual_DONTCARE = (ur"()(?:(?:(?:je\s*)?m|(?:on\s*)?s)'?en?\s*(?:f(?:iche|ou[st])|tape|cogne|branle|bat\s*les\s*couilles)\s*(?:d[ue]s?)?" +
            ur"|(?:c'?e(?:st?|ts?)\s*)?pas?\s*graves?" +
            ur"|[cç]a\s*importe\s*p(?:as?|eu)" +
            ur"|peu[stx]?\s*importe(?:\s*l[ae]s?)?" +
            ur"|(?:j'?\s*en\s*ai\s*)?rien\s*[aà]\s*(?:f(?:out|ai)re|battre|cir[eé]r?)(?:\s*de\s*[cç]a)?" +
            ur"|ba(?:llec|t\s*les\s*couilles|lais?\s*couilles?)(?:\s*fr[eè]re?)?" +
        ")")
        self.contextual_NONE = ur"(?:pas?(?:\s*du\s*tou[stx]?|)|sans|non)"
        self.contextual_LITTLE = ur"(?:(?:une?\s*|tr[eéè]s\s*|extr[eêè]me?m?eent\s*|)peu[st]?|pas?\s*(?:tro[ps]|b(?:eau|o)c(?:ou)?p))"
        self.contextual_FAIR = ur"(?:ass[eé][ez]?|relativement)"
        self.contextual_MUCH = ur"(?:tr[eè]s|biens?|b(?:eau|o)c(?:ou)?p)"
        self.contextual_VERYMUCH = ur"(?:extr[eêè]me?m?ent|[eé]norm[eé]ment|hype?ra?|supe?ra?|m[eé]ga)"
        self.contextual_COMPLETELY = ur"(?:full|tro[ps]|pur)"



    def create_domain_dependent_regex(self):
        """Can overwrite any of the regular expressions set in RegexParser.RegexParser.init_regular_expressions().
        This doesn't deal with slot,value (ie domain dependent) semantics. For those you need to handcraft
        the _decode_[inform,request,confirm] etc.
        """
        # REDEFINES OF BASIC SEMANTIC ACTS (ie those other than inform, request): (likely nothing needs to be done here)
        #eg: self.rHELLO = "anion"

        self._domain_init(dstring=self.domainTag)

        # DOMAIN DEPENDENT SEMANTICS:
        self.slot_vocab = dict.fromkeys(self.USER_REQUESTABLE,'')
        # FIXME: define slot specific language -  for requests
        #---------------------------------------------------------------------------------------------------
        #exit("THESE NEED FIXING FOR THIS DOMAIN")

        self.slot_vocab["kind"] = ur"(type|genre)"
        self.slot_vocab["energy"] = ur"(energ(i(sant)?e|etiques?))"
        self.slot_vocab["fatness"] = ur"((?:tau[stx]\s*de\s*)?grai?ss?e?)"
        self.slot_vocab["sweetness"] = ur"((?:tau[stx]\s*de\s*)?sucree?)"
        self.slot_vocab["saltiness"] = ur"((?:tau[stx]\s*de\s*)?s[ae]le?e?)"
        self.slot_vocab["pieces"] = ur"(?:d[eu]s?\s*)?(pi[eè]ces|nombre\s*de\s*(?:pi[eè]ces|morceaux|st[eè]a?ks|nuggets))"
        self.slot_vocab["meat"] = ur"((?:type\s*de\s*|de\s*la\s*)?viandes?)"
        self.slot_vocab["cheese"] = ur"(?:d[eu]\s*)?(fromage|chedd?ar)"
        self.slot_vocab["bacon"] = ur"(bacon|lard\s*grille)"
        self.slot_vocab["happymealavailable"] = ur"(?:disponible\s*(?:en|dans\s*un)\s*[Hh]appy\s*[Mm]eal)"
        self.slot_vocab["happymealonly"] = ur"(?:(?:disponible\s*)?(?:uniqu|seul)ement\s*(?:disponible\s*)?(?:en|dans\s*un)\s*[Hh]appy\s*[Mm]eal)"
        #---------------------------------------------------------------------------------------------------
        # Generate regular expressions for requests:
        self._set_request_regex()


        # FIXME:  many value have synonyms -- deal with this here:
        self._set_value_synonyms()  # At end of file - this can grow very long
        self._set_inform_regex()


    def _set_request_regex(self):
        """
        """
        self.request_regex = dict.fromkeys(self.USER_REQUESTABLE)
        for slot in self.request_regex.keys():
            # FIXME: write domain dependent expressions to detext request acts
            self.request_regex[slot] = self.rREQUEST+ur"\s*"+self.slot_vocab[slot]
            self.request_regex[slot] += "|"+self.IT+ur"\s*"+self.slot_vocab[slot]

    def _set_inform_regex(self):
        """
        """
        self.inform_absolute = dict.fromkeys(self.USER_INFORMABLE)
        self.inform_contextual = dict.fromkeys(self.USER_REQUESTABLE)

        for slot in self.inform_contextual.keys():
            self.inform_contextual[slot] = {}
            for value in self.slot_values[slot].keys():
                if value == "0":
                    self.inform_contextual[slot][value] = self.contextual_NOT
                elif value == "1":
                    self.inform_contextual[slot][value] = self.contextual_YES
                elif value == "free":
                    self.inform_contextual[slot][value] = self.contextual_NONE
                elif value == "little":
                    self.inform_contextual[slot][value] = self.contextual_LITTLE
                elif value == "fair":
                    self.inform_contextual[slot][value] = self.contextual_FAIR
                elif value == "much":
                    self.inform_contextual[slot][value] = self.contextual_MUCH
                elif value == "enormous":
                    self.inform_contextual[slot][value] = self.contextual_VERYMUCH
                elif value == "full":
                    self.inform_contextual[slot][value] = self.contextual_COMPLETELY
                elif value == "dontcare":
                    self.inform_contextual[slot][value] = self.contextual_DONTCARE
                else:
                    continue
                self.inform_contextual[slot][value] = ur"^\s*" + self.inform_contextual[slot][value] + ur"\s*$"

        for slot in self.inform_absolute.keys():
            self.inform_absolute[slot] = {}
            for value in self.slot_values[slot].keys():
                self.inform_absolute[slot][value] = ur"^\s*(?:" + self.general_INFORM + ur"\s*" +  self.slot_values[slot][value] + ur"|" + self.slot_values[slot][value] + self.WBG + ur")\s*$"

        self.inform_regex = dict.fromkeys(self.USER_INFORMABLE)
        for slot in self.inform_regex.keys():
            self.inform_regex[slot] = {}
            self.inform_regex[slot]['dontcare'] = ''
            for value in self.slot_values[slot].keys():
                self.inform_regex[slot][value] = (self.general_INFORM + ur"\s*" + self.slot_values[slot][value] +
                    ur"|" + self.slot_values[slot][value])
            s = (self.DONTCARE + ur"(?:\s*(?:comment|[aà]\s*quell?e?\s*point?|si)\s*c'?e(?:st?|ts?)\s*(" +
                "|".join([self.slot_values[slot][value] for value in self.slot_values[slot].keys()])
                + ur")(?:\s*ou\s*pas?)?)")

            if (self.inform_regex[slot]['dontcare'] != ''):
                s = "|" + s
            self.inform_regex[slot]['dontcare'] += s


                # FIXME:  Handcrafted extra rules as required on a slot to slot basis:

            # FIXME: value independent rules:


    def _generic_request(self,obs,slot):
        """
        """
        if self._check(re.search(self.request_regex[slot],obs, re.I)):
            self.semanticActs.append('request('+slot+')')

    def _generic_inform(self, obs, slot):
        """
        """
        DETECTED_SLOT_INTENT = False
        '''for value in self.inform_contextual[slot].keys():
            if self._check(re.search(self.inform_contextual[slot][value], obs, re.I)):
                # -> informed !
                print u"Recognized [Contextual] : " + slot + u"::" + value
                pass
            elif self._check(re.search(self.inform_absolute[slot][value], obs, re.I)):
                #informed
                print u"Recognized [Absolute] : " + slot + u"::" + value
                pass
        for other_slot in self.inform_absolute.keys():
            if (other_slot == slot):
                continue
            for value in self.inform_absolute[slot].keys():
                if (self._check(re.search(self.inform_absolute[slot][value], obs, re.I))):
                    print u"Recognized [Absolute|Other(" + slot + u")] : " + other_slot + u"::" + value'''
        obs = re.sub(ur"\s{2,}", ' ', obs)
        for value in self.slot_values[slot].keys():
            if self._check(re.search(self.inform_regex[slot][value],obs, re.I)):
                print slot + "::" + value
                #FIXME:  Think easier to parse here for "dont want" and "dont care" - else we're playing "WACK A MOLE!"
                ADD_SLOTeqVALUE = True
                # Deal with -- DONTWANT --:
                if self._check(re.search(self.rINFORM_DONTWANT + r"\s*" + self.slot_values[slot][value], obs, re.I)):
                    self.semanticActs.append('inform('+slot+'!='+value+')')  #TODO - is this valid?
                    ADD_SLOTeqVALUE = False
                # Deal with -- DONTCARE --:
                elif self._check(re.search(self.rINFORM_DONTCARE + r"\s*" + value, obs, re.I)) and not DETECTED_SLOT_INTENT:
                    self.semanticActs.append('inform('+slot+'=dontcare)')
                    ADD_SLOTeqVALUE = False
                    DETECTED_SLOT_INTENT = True
                # Deal with -- REQUESTS --: (may not be required...)
                #TODO? - maybe just filter at end, so that inform(X) and request(X) can not both be there?
                elif ADD_SLOTeqVALUE and not DETECTED_SLOT_INTENT:
                    self.semanticActs.append('inform('+slot+'='+value+')')

    def _decode_request(self, obs):
        """
        """
        # if a slot needs its own code, then add it to this list and write code to deal with it differently
        DO_DIFFERENTLY= [] #FIXME
        for slot in self.USER_REQUESTABLE:
            if slot not in DO_DIFFERENTLY:
                self._generic_request(obs,slot)
        # Domain independent requests:
        self._domain_independent_requests(obs)


    def _decode_inform(self, obs):
        """
        """
        # if a slot needs its own code, then add it to this list and write code to deal with it differently
        DO_DIFFERENTLY = [] #FIXME
        for slot in self.USER_INFORMABLE:
            if slot not in DO_DIFFERENTLY:
                self._generic_inform(obs,slot)
        # Check other statements that use context
        self._contextual_inform(obs)

    def _decode_type(self,obs):
        """
        """
        # This is pretty ordinary - will just keyword spot for now since type really serves no point at all in our system
        if self._check(re.search(self.inform_type_regex,obs, re.I)):
            self.semanticActs.append('inform(type='+self.domains_type+')')


    def _decode_confirm(self, obs):
        """
        """
        #TODO?
        pass


    def _set_value_synonyms(self):
        """Starts like:
            self.slot_values[slot] = {value:"("+str(value)+")" for value in domain_ontology["informable"][slot]}
            # Can add regular expressions/terms to be recognised manually:
        """
        #FIXME:
        #---------------------------------------------------------------------------------------------------
        #exit("THESE NEED FIXING FOR THIS DOMAIN")

        # TYPE:
        self.inform_type_regex = ur"(ma?cdo(?:nalds?)?|[àa]\s*(?:bouff|mang)er|de\s*la\s*bouffe)"
        # SLOT: area
        slot = 'kind'
        # {u'west': '(west)', u'east': '(east)', u'north': '(north)', u'south': '(south)', u'centre': '(centre)'}
        self.slot_values[slot]['sandwich'] = ur"(?:une?\s*)?(sandwich)e?s?"
        self.slot_values[slot]['accompaniment'] = ur"(une?\s*)?(accompagnement)s?"
        self.slot_values[slot]['drink'] = ur"(?:une?\s*)?(boisson)s?"
        self.slot_values[slot]['dessert'] = ur"(?:une?\s*)?(dessert)s?"
        self.slot_values[slot]['dontcare'] = ur"(?:n'?|peu[st]?)\s*(importe)(?:\s*quel\s*produits?)"
        # SLOT: pricerange
        slot = 'energy'
        value = ur'\s*calori(?:qu|)e?s?'
        self.slot_values[slot]['free'] = ur"(" + self.contextual_NONE + value + ur")"
        self.slot_values[slot]['little'] = ur"(" + self.contextual_LITTLE + value + ur")"
        self.slot_values[slot]['fair'] = ur"(" + self.contextual_FAIR + value + ur")"
        self.slot_values[slot]['much'] = ur"(" + self.contextual_MUCH + value + ur")"
        self.slot_values[slot]['enormous'] = ur"(" + self.contextual_VERYMUCH + value + ur"|(?:un\s*(?:bon\s*)?)?truc\s*de\s*gros)"
        self.slot_values[slot]['dontcare'] = ur"(n'importe\s*quell?e?\s*niveau\s*de\s*calories?)"
        # SLOT: near
        # rely on ontology for now
        # SLOT: hasparking
        slot = 'fatness'
        value = ur'\s*grai?s{0,2}e?'
        any_level = ur"n'importe\s*quell?e?\s*niveau\s*de\s*"
        self.slot_values[slot]['free'] = ur"(" + self.contextual_NONE + value + ur")"
        self.slot_values[slot]['little'] = ur"(" + self.contextual_LITTLE + value + ur")"
        self.slot_values[slot]['fair'] = ur"(" + self.contextual_FAIR + value + ur")"
        self.slot_values[slot]['much'] = ur"(" + self.contextual_MUCH + value + ur")"
        self.slot_values[slot]['enormous'] = ur"(" + self.contextual_VERYMUCH + value + ur"|(?:un\s*(?:bon\s*)?)?truc\s*de\s*gros)"
        self.slot_values[slot]['full'] = ur"(?:du\s*gras\s*pur|" + self.contextual_COMPLETELY + ur")"
        self.slot_values[slot]['dontcare'] = ur"(?:" + any_level + ur"grai?ss?e?)"
        slot = 'sweetness'
        value = ur'\s*sucr[ée]e?s?'
        self.slot_values[slot]['free'] = ur"(" + self.contextual_NONE + ur"\s*sucr[ée])"
        self.slot_values[slot]['little'] = ur"(" + self.contextual_LITTLE + ur"\s*sucr[ée])"
        self.slot_values[slot]['fair'] = ur"(" + self.contextual_FAIR + ur"\s*sucr[ée])"
        self.slot_values[slot]['much'] = ur"(" + self.contextual_MUCH + ur"\s*sucr[ée])"
        self.slot_values[slot]['enormous'] = ur"(" + self.contextual_VERYMUCH + ur"\s*sucr[ée]|(?:un\s*(?:bon\s*)?)?truc\s*de\s*diab[eé]tiques?)"
        self.slot_values[slot]['full'] = ur"(du(?:\s*sucr[ée]\s*pur|diab[eè]te\s*garanti[est]?)|" + self.contextual_COMPLETELY + value + ur")"
        self.slot_values[slot]['dontcare'] = ur"(" + any_level + ur"sucr[ée])"
        slot = 'saltiness'
        value = ur'ur"\s*s(?:al[eé]e?|el)s?'
        self.slot_values[slot]['free'] = ur"(" + self.contextual_NONE + value + ur")"
        self.slot_values[slot]['little'] = ur"(" + self.contextual_LITTLE + value + ur")"
        self.slot_values[slot]['fair'] = ur"(" + self.contextual_FAIR + value + ur")"
        self.slot_values[slot]['much'] = ur"(" + self.contextual_MUCH + value + ur")"
        self.slot_values[slot]['enormous'] = ur"(" + self.contextual_VERYMUCH + value + ur")"
        self.slot_values[slot]['full'] = ur"(du(?:\s*sel?\s*pur)|" + self.contextual_COMPLETELY + value + ur")"
        self.slot_values[slot]['dontcare'] = ur"(" + any_level + ur"s[ea]le?e?s?)"
        slot = 'meat'
        self.slot_values[slot]['n/a'] = ur"(sans|(?:surtou[st]\s*)?pas?\s*de)\s*viandes?"
        self.slot_values[slot]['beef'] = ur"((?:du\s*)(?:boeuf|steak)|de\s*la\s*vache)"
        self.slot_values[slot]['chicken'] = ur"((?:du\s*)?poulet|(?:de\s*la\s*)volaille)"
        self.slot_values[slot]['ham'] = ur"((?:du\s*)?(?:jambon|por[ck]?\b|cochon)|de\s*la\s*cochonailles?)"
        self.slot_values[slot]['fish'] = ur"((?:du\s*)?poisson|(?:de\s*la\s*)poiscaille)"
        self.slot_values[slot]['dontcare'] = ur"(n'importe\s*quell?e?\s*(?:type\s*de\s*)viandes?)"


        slot = 'ishappymealavailable'
        self.slot_values[slot]['0'] = ur"((?:pas?\s*|non\s*|in)disponible\s*en\s*[Hh]appy\s*[Mm]eal)"
        self.slot_values[slot]['1'] = ur"(?<!non\s|pas\s)(?<!non|pas|pa\s)(?<!pa|in)(disponible\s*en\s*[Hh]appy\s*[Mm]eal)"
        self.slot_values[slot]['dontcare'] = ur""
        slot = 'ishappymealonly'
        self.slot_values[slot]['0'] = ur"(disponible\s*(?:hors|sans)\s*[Hh]appy\s*[Mm]eal)"
        self.slot_values[slot]['1'] = ur"((?:disponible\s*)?(?:uniqu|seul)ement\s*(?:disponible\s*)?(?:en|dans\s*un)\s*[Hh]appy\s*[Mm]eal)"
        self.slot_values[slot]['dontcare'] = ur""
        slot = 'hascheese'
        value = ur'\s*fromages?'
        self.slot_values[slot]['0'] = ur"(sans" + value + ur")"
        self.slot_values[slot]['1'] = ur"(avec" + value + ur")"
        self.slot_values[slot]['dontcare'] = ur"(" + self.DONTCARE + ur"\s*(?:du|le|la\s*pr[eé]sence\s*de)" + value + ur")"
        slot = 'hasbacon'
        value = ur'\s*(?:bacon|lar[ds])'
        self.slot_values[slot]['0'] = ur"(sans" + value + ur")"
        self.slot_values[slot]['1'] = ur"(avec" + value + ur")"
        self.slot_values[slot]['dontcare'] = ur"(" + self.DONTCARE + ur"\s*(?:du|le|la\s*pr[eé]sence\s*de)" + value + ur")"

        slot = 'pieces'
        value = ur'\s*(?:pi[eè]ce|stea?k|morceau|nugget)[sx]?'
        self.slot_values[slot]['0'] = ur"(0" + value + ur")"
        self.slot_values[slot]['1'] = ur"(1" + value + ur")"
        self.slot_values[slot]['2'] = ur"(2" + value + ur")"
        self.slot_values[slot]['4'] = ur"(4" + value + ur")"
        self.slot_values[slot]['6'] = ur"(6" + value + ur")"
        self.slot_values[slot]['9'] = ur"(9" + value + ur")"
        self.slot_values[slot]['20'] = ur"(20" + value + ur")"
        self.slot_values[slot]['dontcare'] = ur"(" + self.DONTCARE + ur"\s*(?:du|le)\s*nombre\s*de" + value + ur")"

        for key in self.slot_values['name'].keys():
            s = self.slot_values['name'][key][1:-1]
            s = s.replace('(', r'\(')
            s = s.replace(')', r'\)')
            s = s.replace(' ', r'\s*')
            s = s.replace('\'', r'\'?')
            self.slot_values['name'][key] = ur"(l[ae]s?\s*" + s + ur")"
        # SLOT: stars
        #---------------------------------------------------------------------------------------------------


#END OF FILE
