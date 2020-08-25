from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics import Color
import os
from random import randint
from math import gcd as gcd


def Ascii(text):
    new_text = []
    for item in text:
        new_text.append(ord(item))
    return new_text


def Character(text):
    import codecs
    new_text = []
    for item in text:
        new_text.append(chr(item))
    return new_text


def IsPrime(n):
    for i in range(2, n//2+1):
        if n%i == 0:
            return False
    return True


def GenRandPrime(min, max):
    number = randint(min,max)
    if IsPrime(number):
        return number
    else:
        return GenRandPrime(min, max)


def CoPrime1(a, b):
    return gcd(a, b) == 1


def CoPrime2(e, modulus, phifunction):
    if CoPrime1(e, modulus) and CoPrime1(e, phifunction):
        return True
    else:
        return False


def gen_public_key(modulus, phifunction):
    e = randint (1, phifunction)
    if CoPrime2(e, modulus, phifunction):
        return e
    else:
        return gen_public_key(modulus, phifunction)


def gen_private_key(public_key, phifunction):
    for i in range(phifunction * 100):
        if (i * public_key) % phifunction == 1:
            d1 = i
            break
    random_factor = randint(1, 5)
    private_key = d1 * ((phifunction * random_factor) + 1)
    return private_key


def Encrypt(message, public_key, modulus):
    return (message ** public_key) % modulus


def GenerateKeys():
    global Public_Key_Actual
    global Private_Key_Actual
    global Modulus_Actual
    Prime1 = GenRandPrime(2, 50)
    Prime2 = GenRandPrime(2, 50)
    Modulus_Actual = Prime1 * Prime2
    Phi_Funcion = (Prime1 - 1) * (Prime2 - 1)
    Public_Key_Actual = gen_public_key(Modulus_Actual, Phi_Funcion)
    Private_Key_Actual = gen_private_key(Public_Key_Actual, Phi_Funcion)


class MainWindow(Screen):
    pass


class LoadDialog(FloatLayout):

    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class EncryptionScreen(Screen):

    def __init__(self, **kwargs):
        super(EncryptionScreen, self).__init__(**kwargs)
        GenerateKeys()
        self.Privato_key = Private_Key_Actual
        self.Publuco_key = Public_Key_Actual
        self.Modululo = Modulus_Actual


    def new(self):
        self.same = Label(text='Encryption Successful!\nWould you\nlike to\nencrypt another\nfile with the\nsame key?',
         color=[130/255, 120/255, 98/255, 1], size_hint= (1, .5), pos_hint={'y':.5},
         font_name='DoHyeon-Regular', font_size=30, halign="center")

        with self.same.canvas.before:
            Color(218/255, 193/255, 151/255, 1)
            self.rect = Rectangle(size=(self.width*1, self.height*.4), pos=(0, self.height*.5))
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.namee.add_widget(self.same)
        self.namee.remove_widget(self.removable)
        self.namee.remove_widget(self.key)
        self.namee.remove_widget(self.newky)


        self.yesb = Button(text='Yes', size_hint=(.5, .5), pos_hint={'x': .5}, font_size=30,
         font_name='DoHyeon-Regular', background_normal='', background_color=[166/255, 224/255, 185/255, 1], 
         color=[130/255, 120/255, 98/255, 1])
        self.yesb.bind(on_press=self.restore)

        self.nob = Button(text='No', size_hint=(.5, .5), font_size=30,
         font_name='DoHyeon-Regular', background_normal='', background_color=[166/255, 224/255, 185/255, 1], 
         color=[130/255, 120/255, 98/255, 1])
        self.nob.bind(on_press=self.restore)
        self.nob.bind(on_press=self.nw_kys)

        self.namee.add_widget(self.nob)
        self.namee.add_widget(self.yesb)


    def restore(self, instance):
        self.namee.remove_widget(self.same)
        self.namee.remove_widget(self.yesb)
        self.namee.remove_widget(self.nob)
        self.namee.add_widget(self.removable)
        self.namee.add_widget(self.key)
        self.namee.add_widget(self.newky)


    def nw_kys(self, instnace):
        GenerateKeys()
        self.Privato_key = Private_Key_Actual
        self.Publuco_key = Public_Key_Actual
        self.Modululo = Modulus_Actual
        self.key.text = 'The private\nkey will be\n{},{}'.format(self.Privato_key, self.Modululo)


    def nw_kyst(self):
        GenerateKeys()
        self.Privato_key = Private_Key_Actual
        self.Publuco_key = Public_Key_Actual
        self.Modululo = Modulus_Actual
        self.key.text = 'The private\nkey will be\n{},{}'.format(self.Privato_key, self.Modululo)


    def update_rect(self, *args):
        self.rect.pos = 0, self.height*.5
        self.rect.size = self.width*1, self.height*.4


    def dismiss_popup(self):
        self._popup.dismiss()


    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.file_contents = stream.read()
        self.file_contents = Ascii(self.file_contents)
        for i in range(len(self.file_contents)):
            self.file_contents[i] = str(Encrypt(self.file_contents[i], self.Publuco_key, self.Modululo))
        self.file_contents = ','.join(self.file_contents)
        self.Ecrypted_File = open(os.path.join(path, filename[0]), 'w')
        self.Ecrypted_File.write(self.file_contents)
        self.Ecrypted_File.close()
        self.new()

        self.dismiss_popup()


class DecryptionScreen(Screen):

    def private_key_ask(self):
        
        self.private_key = Label(text='What is\nthe private\nkey?',
         color=[130/255, 120/255, 98/255, 1], size_hint=(1, .5), pos_hint={'y':.5},
         font_name='DoHyeon-Regular', font_size=30, halign="center")

        with self.private_key.canvas.before:
            Color(218/255, 193/255, 151/255, 1)
            self.rect = Rectangle(size=(self.width*1, self.height*.4), pos=(0, self.height*.5))
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.private_key_input = TextInput(multiline=False, size_hint=(1, .4), pos_hint={'y': .1})

        self.submit = Button(text='Submit', size_hint=(1, .1), 
         font_name='DoHyeon-Regular', font_size=30, halign="center")
        self.submit.bind(on_press=self.decrypt)

        self.decryption.add_widget(self.submit)
        self.decryption.add_widget(self.private_key)
        self.decryption.remove_widget(self.select)
        self.decryption.add_widget(self.private_key_input)
    

    def restore(self):
        self.decryption.remove_widget(self.submit)
        self.decryption.remove_widget(self.private_key)
        self.decryption.add_widget(self.select)
        self.decryption.remove_widget(self.private_key_input)


    def decrypt(self, instance):
        self.privato_key = self.private_key_input.text
        self.privato_key = self.privato_key.split(',')
        for i in range(len(self.file_contents)):
            self.file_contents[i] = Encrypt(int(self.file_contents[i]), int(self.privato_key[0]), int(self.privato_key[1]))
        self.file_contents = Character(self.file_contents)
        self.file_contents = ''.join(self.file_contents)
        self.Decrypted_File = open(os.path.join(self.path, self.file_name), 'w')
        self.Decrypted_File.write(self.file_contents)
        self.Decrypted_File.close()
        self.restore()


    def update_rect(self, *args):
        self.rect.pos = 0, self.height*.5
        self.rect.size = self.width*1, self.height*.4


    def dismiss_popup(self):
        self._popup.dismiss()


    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.file_contents = stream.read()
        self.file_contents = self.file_contents.split(',')
        self.file_name = filename[0]
        self.path = path

        self.dismiss_popup()
        self.private_key_ask()



class WindowManager(ScreenManager):
    pass


class FileSelector(GridLayout):
    pass


kv = Builder.load_file('blacko.kv')


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()