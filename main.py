

""""
"""
import json
from tkinter import *
from tkinter import messagebox, scrolledtext
import tkinter.ttk as ttk
import keys
import time
# Trying to import modules that needs installation and install them if not installed
try:
    from ibm_watson import ToneAnalyzerV3, ApiException
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from win10toast import ToastNotifier
    from PIL import ImageTk, Image
except ImportError as e:
    packages =["pillow", "ibm-watson>=4.7.1", "win10toast"]
    from pip._internal import main as install
    for package in packages:
        install(["install", package])
    else:
        pass
finally:
    pass
# Exceptions
class MinimumWordsException(Exception):
    pass
class NullTextException(Exception):
    pass
# Configuring the tone Analyiser
authenticator = IAMAuthenticator(f'{keys.API_KEY}')
tone_analyzer = ToneAnalyzerV3(
    version=f'{keys.VERSION}',
    authenticator=authenticator
)
tone_analyzer.set_service_url(f'{keys.URL}')

#  Configuring the notifier
toaster = ToastNotifier()
root = Tk()
window_width, window_height = 550, 310
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
position_top, position_right = int(screen_height/2 - window_height/2), int(screen_width/2 - window_width/2)
root.title("Tone Analyzer")
root.geometry('{}x{}+{}+{}'.format(window_width, window_height, position_right, position_top))
root.iconbitmap('main.ico')
root.resizable(False, False)

# Functions

def close():
    confirm = messagebox.askyesnocancel("Closing Tone Analyzer", "Are you sure you want to close Tone Analyzer?", )
    return root.destroy() or root.quit() if confirm else root.focus()
def clear():
    confirm = messagebox.askyesnocancel("Closing Tone Analyzer", "By Clearing the text in the Text Field you will "
                                                                 "lose all the infomation that you have typed. "
                                                                 "Confirm to continue!")
    return text.delete('0.0', END) if confirm else text.focus() or root.focus()

def analyze():
    # if len(text.get('0.0', END)) != 0:
    #     text.delete('0.0', END)
    text_to_be_analysed = text.get('0.0', END)
    # check if the text has less than one word
    try:
        if len(str(text_to_be_analysed)) == 0:
            raise NullTextException("We can not analyse a null text.")
        elif  len(str(text_to_be_analysed).split(' ')) == 1 or len(str(text_to_be_analysed).split(' ')) ==2:
            print(str(text_to_be_analysed).split(' '))
            # raise MinimumWordsException("We can not analyse your tone because your words are few.")
        else:
            # Analyze the tone.
            try:
                tone_analysis = tone_analyzer.tone(
                    {'text': text_to_be_analysed},
                ).get_result()
                try:
                    #  for multiple sentence
                    for sentences_tone in tone_analysis['sentences_tone']:
                        time.sleep(2)
                        toaster.show_toast("Tone Analyzer",
                                           f'{sentences_tone["text"]}\n -{str(sentences_tone["tones"][0]["tone_name"]).upper()}',
                                           icon_path="main.ico",
                                           duration=5, threaded= not False)
                    return
                except Exception:
                    #  for single sentence
                    print(json.dumps(tone_analysis, indent=2))
                    toaster.show_toast("Tone Analyzer",
                                       f'{text_to_be_analysed}\n\n -'
                                       f'{str(tone_analysis["document_tone"]["tones"][0]["tone_name"]).upper()}',
                                       icon_path="main.ico",
                                       duration=5, threaded=True)
            except ApiException as e:
                print(e)
            finally:
                pass
    except MinimumWordsException or NullTextException as e:
        messagebox.showerror("Tone Analyzer", e)
    return
# UI
image = ImageTk.PhotoImage(Image.open('main.ico'))
Label(root, image=image).grid(row=0, column=0, columnspan = 5)
Label(root, text="Type Text Below", fg="lightseagreen", font=("arial", 12, "bold")).grid(row=1, column=0, columnspan
= 5, pady=5)
text = scrolledtext.ScrolledText(root, width=58, height=5, font=("Arial", 12), bg='seagreen', fg="white")
text.grid(row=2, column=0, columnspan= 5, padx=5)
Button(root, command=clear ,width=15, activebackground="pink", text="Clear", bg="orange", bd=1, relief=SOLID, \
                                                                                                      fg="white", pady=5).grid(
    row=3,                                                                                                column=0)
Button(root,width=15, command=close ,activebackground="pink", text="Close", bg="red", bd=1, relief=SOLID, fg="white", \
                                                                                                   pady=5).grid(
    row=3, column=2, pady=10)
Button(root, command=analyze, width=15, activebackground="pink", text="Analyze", bg="lightseagreen", bd=1,
       relief=SOLID,
       fg="white",
       pady=5).grid(row=3, column=4)

root.mainloop(0)
