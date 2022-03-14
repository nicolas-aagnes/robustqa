from googletrans import Translator, constants
import json
from pathlib import Path
import copy


def back_translate(datasets,datadir,lang):
    datasets = datasets.split(",")
    l = len(datasets)
    print("Working with language ",lang)
    for i,dataset in enumerate(datasets):
        path = Path(f'{datadir}/{dataset}')
        with open(path, 'rb') as f:
            squad_dict = json.load(f)
        Ldata =[]
        for group in squad_dict['data']:

            passage =(group['paragraphs'])[0]
            context = passage['context']

            for qa in passage['qas']:
                question = qa['question']
                if len(qa['answers']) == 0:
                    translate_all =True
                    idx=0
                    txt =""
                    new_context, new_idx = backtranslate(context, idx, txt, lang, translate_all)
                    new_paragraph = {"paragraphs": [{"context": new_context,
                                                     "qas": [{"question": question,
                                                              "answers": [],
                                                              "id": qa["id"] + lang}]}]}
                    Ldata.append(new_paragraph)

                else:
                    for i,answer in enumerate(qa['answers']):
                        idx = answer["answer_start"]
                        translate_all = False
                        txt  = answer["text"]
                        new_context, new_idx = backtranslate(context, idx, txt, lang, translate_all)
                        new_paragraph = {"paragraphs": [{"context": new_context,
                                                         "qas": [{"question": question,
                                                                  "answers": [{"answer_start": new_idx, "text": txt}],
                                                                  "id": qa["id"] +str(i)+ lang}]}]}

                        Ldata.append(new_paragraph)

        back_translated = {"data":Ldata}


        new_dataset_name = "datasets/oodomain_train/"+dataset+"_backtranslate_"+lang
        with open(new_dataset_name, "w") as outfile:
            json.dump(back_translated, outfile)


def backtranslate(passage,idx,txt,lang,translate_all=False):
    translator = Translator()
    if translate_all:

        translations = translator.translate(passage, dest=lang).text
        back_transl = translator.translate(translations, src=lang, dest="en").text
    else:
        answerLen = len(list(txt))
        c2 = copy.deepcopy(passage)
        c2list = list(c2)
        #print("c2list",c2list)
        c2_2answer = "".join(c2list[:idx])
        c2_post_answer = "".join(c2list[idx + answerLen:])
        answer = txt
        assert (idx + answerLen < len(c2list)+1)
        if idx>0 and idx+answerLen<len(c2list):

            translations_pre = translator.translate(c2_2answer, dest=lang).text
            back_transl_pre = translator.translate(translations_pre, src=lang, dest="en").text

            translations_post = translator.translate(c2_post_answer, dest=lang).text
            back_transl_post = translator.translate(translations_post, src=lang, dest="en").text


            back_transl_pre = (back_transl_pre.encode("ascii", "ignore")).decode()
            back_transl_post = (back_transl_post.encode("ascii", "ignore")).decode()

            back_transl = back_transl_pre+" "+answer+" "+back_transl_post


        elif idx==0:
            translations_post = translator.translate(c2_post_answer, dest=lang).text
            back_transl_post = translator.translate(translations_post, src=lang, dest="en").text

            back_transl_post = (back_transl_post.encode("ascii", "ignore")).decode()

            back_transl = answer + " " + back_transl_post

        elif idx+answerLen ==len(c2list):
            translations_pre = translator.translate(c2_2answer, dest=lang).text
            back_transl_pre = translator.translate(translations_pre, src=lang, dest="en").text

            back_transl_pre = (back_transl_pre.encode("ascii", "ignore")).decode()

            back_transl = back_transl_pre + " " + answer



        if idx==0:
            new_idx =0
        else:
            new_idx = len(list(back_transl_pre))+1

    return back_transl,new_idx

L = ["fr","da","it","es","nl","pt","sv","de","no","ru"]
for lang in L:
    back_translate("duorc,race,relation_extraction","datasets/oodomain_train",lang)