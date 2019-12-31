###############################################################################
# PyDial: Multi-domain Statistical Spoken Dialogue System Software
###############################################################################
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*
# coding: utf-8
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
RegexSemI_Laptops6.py - regular expression based Laptops6 SemI decoder
===============================================================


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


class RegexSemI_Phone(RegexSemI.RegexSemI):
    """
    """
    def __init__(self, repoIn=None):
        RegexSemI.RegexSemI.__init__(self)  #better than super() here - wont need to be changed for other domains
        self.domainTag = "Phone"  #FIXME
        self.create_domain_dependent_regex() 

    def create_domain_dependent_regex(self):
        """Can overwrite any of the regular expressions set in RegexParser.RegexParser.init_regular_expressions(). 
        This doesn't deal with slot,value (ie domain dependent) semantics. For those you need to handcraft 
        the _decode_[inform,request,confirm] etc.
        """
        # REDEFINES OF BASIC SEMANTIC ACTS (ie those other than inform, request): (likely nothing needs to be done here)
        #eg: self.rHELLO = "anion"

        self._domain_init(dstring=self.domainTag)
        
        # DOMAIN DEPENDENT SEMANTICS:
        self.slot_vocab= dict.fromkeys(self.USER_REQUESTABLE,'')
        # FIXME: define slot specific language -  for requests
        #-------------------------------------------------------------------------------------------    
        self.slot_vocab["price"] = "(price|cost|expense|prix|tarif)(?!(\ ?range))"
        self.slot_vocab["pricerange"] = "(price|prix\ ?range)"
        self.slot_vocab["dimension"] = "(size|dimension|taille)"
        self.slot_vocab["weight"] = "(weight|poids)(?!(\ ?range))"
        self.slot_vocab["weightrange"] = "(weight|weight|poids\ ?range)"
        self.slot_vocab["batteryrating"] = "(battery|battery|batterie\ ?rating|rating|estimation\ of\ the\ (laptops\ )*battery)"
        #self.slot_vocab["isforbusinesscomputing"] = "(business\ computing|gaming|fun|games|work|play)"
        #self.slot_vocab["isforbusinesscomputing"] =ur"(?:disponible\s*(?:en|dans\s*un)\s*[Hh]appy\s*[Mm]eal)"
        self.slot_vocab["drive"] = "(drive|hard|disque\ *drive)(?!(\ ?range))"
        self.slot_vocab["driverange"] = "(hard\ *)*drive(\ ?range)"
        self.slot_vocab["name"] = "(name|nom)"
        self.slot_vocab["family"] = "(family|class|marque)"
        self.slot_vocab["couleur"] = "(couleur|rouge|bleu|noir|gris|blanc|or)"
        self.slot_vocab["processeur"] = "(processeur|vitesse|rapide)"
        self.slot_vocab["photo"] = "(photo|appareil|pixel|pixels)"
        #-------------------------------------------------------------------------------------------    
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
            self.request_regex[slot] = self.rREQUEST+"\ "+self.slot_vocab[slot]
            self.request_regex[slot] += "|(?<!"+self.DONTCAREWHAT+")(?<!want\ )"+self.IT+"\ "+self.slot_vocab[slot]
            self.request_regex[slot] += "|(?<!"+self.DONTCARE+")"+self.WHAT+"\ "+self.slot_vocab[slot]

        # FIXME:  Handcrafted extra rules as required on a slot to slot basis:
        self.request_regex["price"] = "(quel\ est\ son\ tarif)|(how\ much\ is\ it)"
        self.request_regex["dimension"] = "(quel\ est\ sa\ dimension)|(how\ big\ is\ it)"
        self.request_regex["weightrange"] = "(quel\ est\ sa\ masse)|(how\ heavy\ is\ it)"
	self.request_regex["drive"] = "(quel\ est\ son\ disque)|(what\ is\ its\ drive\ size)"
	self.request_regex["couleur"] = "(quel\ est\ sa\ couleur)|(how\ heavy\ is\ it)"

    def _set_inform_regex(self):
        """
        """
        self.inform_regex = dict.fromkeys(self.USER_INFORMABLE)
        for slot in self.inform_regex.keys():
            self.inform_regex[slot] = {}
            for value in self.slot_values[slot].keys():
                self.inform_regex[slot][value] = self.rINFORM+"\ "+self.slot_values[slot][value]
                self.inform_regex[slot][value] += "|"+self.slot_values[slot][value] + self.WBG
                self.inform_regex[slot][value] += "|a\ (laptop\ with(\ a)*\ )*" +self.slot_values[slot][value]
                self.inform_regex[slot][value] += "|((what|about|which)(\ (it\'*s*|the))*)\ "+slot+"(?!\ (is\ it))" 
                self.inform_regex[slot][value] += "|(\ |^)"+self.slot_values[slot][value] + "(\ (please|and))*"


                # FIXME:  Handcrafted extra rules as required on a slot to slot basis:

            # FIXME: value independent rules: 
            if slot == "pricerange":
                self.inform_regex[slot]['dontcare'] = "any\ (price|price(\ |-)*range)" 
                self.inform_regex[slot]['dontcare'] +=\
                        "|(don\'*t|do\ not)\ care\ (what|which|about|for)\ (the\ )*(price|price(\ |-)*range)"
            if slot == "weightrange":
                self.inform_regex[slot]['dontcare'] = "any\ (weight|weight(\ |-)*range)"
                self.inform_regex[slot]['dontcare'] +=\
                        "|(don\'*t|do\ not)\ care\ (what|which|about|for)\ (the\ )*(weight|weight(\ |-)*range)"
                self.inform_regex[slot]['dontcare'] += "|"+r"((dont\ care\ how\ heavy){1,1}\ it\ is)"
            if slot == "batteryrating":
                self.inform_regex[slot]['dontcare'] = "any\ (battery|battery(\ |-)*(range|rating))"
                self.inform_regex[slot]['dontcare'] +=\
                        "|(don\'*t|do\ not)\ care\ (what|which|about|for)\ (the\ )*(battery|battery(\ |-)*(range|rating))"
            if slot == "driverange":
                self.inform_regex[slot]['dontcare'] = "any\ (hard\ )*(drive|drive(\ |-)*(range|rating))"
                self.inform_regex[slot]['dontcare'] +=\
                    "|(don\'*t|do\ not)\ care\ (what|which|about|for)\ (the\ )*(hard\ )*(drive|drive(\ |-)*(range|rating))"


    def _generic_request(self,obs,slot):
        """
        """
        if self._check(re.search(self.request_regex[slot],obs, re.I)):
            self.semanticActs.append('request('+slot+')')

    def _generic_inform(self,obs,slot):
        """
        """
        DETECTED_SLOT_INTENT = False
        for value in self.slot_values[slot].keys():
            if self._check(re.search(self.inform_regex[slot][value],obs, re.I)):
                #FIXME:  Think easier to parse here for "dont want" and "dont care" - else we're playing "WACK A MOLE!"
                ADD_SLOTeqVALUE = True
                # Deal with -- DONTWANT --:
                if self._check(re.search(self.rINFORM_DONTWANT+"\ "+self.slot_values[slot][value], obs, re.I)): 
                    self.semanticActs.append('inform('+slot+'!='+value+')')  #TODO - is this valid?
                    ADD_SLOTeqVALUE = False
                # Deal with -- DONTCARE --:
                if self._check(re.search(self.rINFORM_DONTCARE+"\ "+slot, obs, re.I)) and not DETECTED_SLOT_INTENT:
                    self.semanticActs.append('inform('+slot+'=dontcare)')
                    ADD_SLOTeqVALUE = False
                    DETECTED_SLOT_INTENT = True
                # Deal with -- REQUESTS --: (may not be required...)
                #TODO? - maybe just filter at end, so that inform(X) and request(X) can not both be there?
                if ADD_SLOTeqVALUE and not DETECTED_SLOT_INTENT:
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
        DO_DIFFERENTLY= [] #FIXME 
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
        #-------------------------------------------------------------------------------------------    
        # TYPE:
        self.inform_type_regex = r"(phone|telephone|smartphone)"
        # SLOT: family
        slot = 'family'
        # {u'satellite': '(satellite)', u'satellite pro': '(satellite pro)', u'tecra': '(tecra)', u'portege': '(portege)'}
        self.slot_values[slot]['i phone'] = "((marque\ |type\ )*(i\ phone|iphone|apple|pomme))"
        self.slot_values[slot]['samsung'] = "((marque\ |type\ )*(Samsung|samsung|SGH|sgh|sg))"
        self.slot_values[slot]['lg'] = "((to\ be\ |in|any|of)\ )*(tecra)"
        self.slot_values[slot]['huawei'] = "((to\ be\ |in|any|of)\ )*(portege)"
        self.slot_values[slot]['dontcare'] = "any\ family"
        # SLOT: pricerange
        slot = 'pricerange'
        # {u'moderate': '(moderate)', u'budget': '(budget)', u'expensive': '(expensive)'}
        self.slot_values[slot]['moderate'] = "(to\ be\ |any\ )*(moderate|moderately\ priced|mid|middle|average)"
        self.slot_values[slot]['moderate']+="(?!(\ )*weight)"
        self.slot_values[slot]['budget'] = "(to\ be\ |any\ )*(budget|cheap|bargin|cheapest|low\ cost)"
        self.slot_values[slot]['expensive'] = "(to\ be\ |any\ )*(expensive|expensively|dear|costly|pricey)"
        self.slot_values[slot]['dontcare'] = "any\ (price|price(\ |-)*range)"
        # SLOT: batteryrating
        slot = 'batteryrating'
        # {u'exceptional': '(exceptional)', u'good': '(good)', u'standard': '(standard)'}
        self.slot_values[slot]['exceptional'] = "(exceptionelle|meilleur|parfait|best|super)"
        self.slot_values[slot]['good'] = "(bonne|good)"
        self.slot_values[slot]['standard'] = "(standard|moyen)"
        self.slot_values[slot]['dontcare'] = "(peu\ importe|quelquesoit\ la\ batterie|dontcare)"
        # SLOT: weightrange
        slot = 'weightrange'
        # {u'light weight': '(light weight)', u'mid weight': '(mid weight)', u'heavy': '(heavy)'}
        self.slot_values[slot]['light weight'] = "(leger|de\ poids\ leger|light|light\ weight)"
        self.slot_values[slot]['mid weight'] = "(moyen|de\ poids\ moyen|mid|mid\ weight)"
        self.slot_values[slot]['heavy'] = "(lourd| de\ poids\ lourd)"
        self.slot_values[slot]['dontcare'] = "(peu\ importe|quelquesoit\ le\ poids|dontcare)"
        # SLOT: isforbusinesscomputing
        slot = 'isforbusinesscomputing'
        # {u'1': '(1)', u'0': '(0)'}
        WORK ="(work|business|professionnelle|travail|boulot|(my\ )*job)"
        FUN = "(fun|games|play|gaming|leisure|home|jeux|personnelle)"
        #self.slot_values[slot]['1'] = "((?<!(is\ it\ ))((used\ )*for\ "+WORK+"))"
        # Next 2 create problems - copied from Phoenix basically. --TODO - DELETE THEM
        #self.slot_values[slot]['1'] += "|(?<!(is\ it\ ))(i\ want\ it\ for\ "+WORK+"(\ computing)*)"
        #self.slot_values[slot]['1'] += "|((it\'*s*|it\ is)\ for\ "+WORK+"(\computing)*))"
        #self.slot_values[slot]['0'] = "(no\ business\ computing|not\ (used\ )*(for\ )*business(\ computing)*"
        #self.slot_values[slot]['0']+="|i\ want\ a\ gaming(\ laptop)*|(i\ want\ it\ )*for\ )"+FUN
        #self.slot_values[slot]['0'] = ur"(disponible\s*(?:hors|sans)\s*[Hh]appy\s*[Mm]eal)"
        self.slot_values[slot]['1']="oui"
        self.slot_values[slot]['0']="non"
        # SLOT: driverange
        slot = 'driverange'
        # {u'small': '(small)', u'large': '(large)', u'medium': '(medium)'}
        self.slot_values[slot]['small'] = "(small|little|petite|petit)*(disque|driver|disk)"
        self.slot_values[slot]['large'] = "(large|big|lots|grande|super)*(disque|driver|disk)"
        self.slot_values[slot]['medium'] = "(medium|average|moyenne|moyen)*(disque|driver|disk)"
        self.slot_values[slot]['dontcare'] = "(peu\ importe|quel\ que\ soit\ le\ disque|dontcare)"
	slot = 'processeur'
	self.slot_values[slot]['rapide'] = "(rapide|fast)*(processeur|processor)"
        self.slot_values[slot]['moyen'] = "(average|moyenne|moyen)*(processeur|processor)"
        self.slot_values[slot]['bon'] = "(bon|good)*(processeur|processor)"
        self.slot_values[slot]['dontcare'] = "(peu\ importe|quel\ que\ soit\ le\ disque|dontcare)"
	slot = 'photo'
	self.slot_values[slot]['super'] = "(super|parfaite|excellente)*(resolution|photo)"
        self.slot_values[slot]['acceptable'] = "(photo)*(acceptable|medium|average|moyenne|moyen)*(resolution|photo)"
        self.slot_values[slot]['bonne'] = "(bonne|good)*(resolution|photo)"
        self.slot_values[slot]['dontcare'] = "(peu\ importe|quel\ que\ soit\ le\ disque|dontcare)"
	slot= 'couleur'
	self.slot_values[slot]['noir'] = "(noir|noire|black)"
        self.slot_values[slot]['rouge'] = "(rouge|red)"
        self.slot_values[slot]['gris'] = "(gris|gray|grise)"
	self.slot_values[slot]['or'] = "(or|gold)"
        self.slot_values[slot]['bleu'] = "(bleu|bleue|blue)"
	self.slot_values[slot]['blanc'] = "(blanc|white)"
        self.slot_values[slot]['dontcare'] = "(peu\ importe|quel\ que\ soit\ le\ disque|dontcare)"
        #-------------------------------------------------------------------------------------------    



#END OF FILE
