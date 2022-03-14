import sys
import os, re
from googletrans import Translator
from glob import glob

def is_not_blank(s):
    return bool(s and not s.isspace())

def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)
    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

def main():

    ##Working on macos
    ## change / to \ to work on windows platform

    input_validation = output_validation = True
    while (input_validation):
        input_folder = input("Enter root input folder: (default: /Users/joaosobral/Desktop/XAMLtranslator)\n- ")
        if (input_folder == ""):
            input_folder = '/Users/joaosobral/Desktop/XAMLtranslator'
        if (os.path.isdir(input_folder)):
            input_validation = False
        else:
            print("invalid folder")

    while (output_validation):
        output_folder = input("Enter output folder: (default: /Users/joaosobral/Desktop/XAMLtranslator) \n- ")
        if (output_folder == ""):
            output_folder = '/Users/joaosobral/Desktop/XAMLtranslator'
        if (os.path.isdir(output_folder)):
            output_validation = False
        else:
            print("invalid folder")

    ext = input("File Extension: (default: .xaml ) \n- ")
    if (not ext):
        ext = ".xaml"

    input_lang = input("Input Language: (default: Pt ) \n- ")
    if (not input_lang):
        input_lang = "Pt"

    output_lang = input("Output Language: (default: En ) \n- ")
    if (not output_lang):
        output_lang = "En"

    subfolders, files = run_fast_scandir(input_folder, [ext])

    print(f"Found files: {len(files)}. Found subfolders: {len(subfolders)}")

    if len(files) < 1:
        print("No Files to be converted")
        return

    fails = []
    completed = []
    for file in files:
        try:
            print("translating " + file)
            str = file[len(input_folder):]
            output_file = f"{output_folder}/{output_lang}.xaml"
            output_dir = output_file.rsplit('/', 1)[0]
            try:
                os.makedirs(output_dir)
            except:
                pass

            input_text = open(file, 'r').read()

            bracket_open = False
            output_text = ""
            text_to_translate = ""
            for i in range(len(input_text)):
                if (input_text[i] == ">"):
                    text_to_translate = ""
                    output_text = output_text + input_text[i]
                    bracket_open = True
                elif (input_text[i] == "<" and bracket_open):
                    translator = Translator()

                    if is_not_blank(text_to_translate):
                        ##special chars

                        #   <	&lt;	Less than symbol.'<>&"\''
                        #   >	&gt;	Greater than sign.
                        #   &	&amp;	Ampersand symbol.
                        #   "	&quot;	Double quote symbol.
                        #   '	&apos;	Single quote symbol.

                        text_to_translate = text_to_translate.replace("&lt;", "<")
                        text_to_translate = text_to_translate.replace("&gt;", ">")
                        text_to_translate = text_to_translate.replace("&amp;", "&")
                        text_to_translate = text_to_translate.replace("&quot;", '\"')
                        text_to_translate = text_to_translate.replace("&apos;", "'")

                        translation = translator.translate(text_to_translate, dest='en')
                        ##special chars

                        text_to_translate = text_to_translate.replace("<","&lt;")
                        text_to_translate = text_to_translate.replace( ">", "&gt;")
                        text_to_translate = text_to_translate.replace( "&", "&amp;")
                        text_to_translate = text_to_translate.replace( '\"', "&quot;")
                        text_to_translate = text_to_translate.replace("'", "&apos;")

                        print(f"{text_to_translate} -> {translation.text}")
                        output_text = output_text + translation.text
                    else:
                        output_text = output_text + text_to_translate

                    output_text = output_text + input_text[i]
                    bracket_open = False
                elif (bracket_open):
                    text_to_translate = text_to_translate+input_text[i]
                else:
                    output_text = output_text+input_text[i]


            #special chars convertion

            with open(output_file, "w") as text_file:
                print(output_text, file=text_file)

            completed.append(file)
        except Exception as e:
            fails.append(file)
            print(e)

    print(f"Completed files: {len(completed)}. Fails: {len(fails)}")
    if (len(fails) > 0):
        print("Failed Files:")
        for i in fails:
            print(i)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
