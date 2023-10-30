from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.graphics.transformation import Matrix
import math
from kivy.uix.button import Button
from kivy.animation import Animation
import random
from kivy.uix.floatlayout import FloatLayout
import os
from kivy.utils import platform
from AppKit import NSApplication, NSWindow, NSFloatingWindowLevel, NSUserNotification, NSUserNotificationCenter, NSUserNotificationDefaultSoundName
import time
from kivy.graphics import Color, Rectangle
import statistics

Window.size=(450,300)
darkblack= (4,12,9)
black= (4,30,30)
shadeblack=(11,29,30)
darkgreen= (20, 50, 45)
forestgreen=(33,76,65)
lightgreen=(128,167,142)
lightestgreen=(197,219,202)

title_text="Get Ready"
time_text="1:00"
break_text=""

class ObjEntry(FloatLayout):
    all_data=[]
    count=0

    def get_entries(self):
        ObjEntry.count+=1
        self.data={"task":self.ids.task.text, "time": self.ids.time.text, "priority": int(self.ids.priority.text)}
        if self.data["priority"]==ObjEntry.count:
            ObjEntry.all_data.append(self.data)
        else:
            ObjEntry.all_data.insert(self.data["priority"]-1,self.data)
        ObjEntry.reorder()
        print(ObjEntry.all_data)
        print(self.data)


    @staticmethod
    def reorder():
        templist=[]
        for i in range(ObjEntry.count):
            ObjEntry.all_data[i]["priority"] = i + 1





class MLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.val_x=random.randint(-10000,10000)/10000
        self.val_y=math.sqrt(1-self.val_x**2)
    def change_dir(self, position):
        if position == 'y':
            self.val_y=-self.val_y
        else:
            self.val_x=-self.val_x


class SpcLabel(Button):

    def on_touch_down(self, touch):
        super(Label, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        super(Label, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        super(Label, self).on_touch_up(touch)

    def on_press(self):
        pass

    def on_release(self):
        pass


class SctrLay(ScatterLayout):
    def __init__(self, **kwargs):
        super(SctrLay, self).__init__(**kwargs)
        self.sizex=1
        self.countbreaths=0
        self.label=Label(size_hint=(1,1))
        self.label2=Label(text="Breath In", color=(0.9,0.9,0.9,0), font_size='50sp')
        self.label3=Label(text="Breath Out", color=(0.9,0.9,0.9,0), font_size='50sp')
        self.add_widget(self.label)
        self.add_widget(self.label2)
        self.add_widget(self.label3)

    def on_animation_progress(self, *args):
        if int(args[-1]*1000)==600:
            self.animate_breath=Animation(color=(0.9,0.9,0.9,0), duration=1, t='out_quad')
            self.animate_breath.start(self.label2)
            self.animate_breath2 = Animation(color=(0.9, 0.9, 0.9, 1), duration=1, t='in_quad')
            self.animate_breath2.start(self.label3)
        elif int(args[-1]*1000)==999:
            self.animate_breath = Animation(color=(0.9, 0.9, 0.9, 1), duration=1, t='in_quad')
            self.animate_breath.start(self.label2)
            self.animate_breath2 = Animation(color=(0.9, 0.9, 0.9, 0), duration=1, t='out_quad')
            self.animate_breath2.start(self.label3)


    def animate_background_color(self, widget, state):
        if self.count==0:
            print("hello")
            self.label2.color=(0.9,0.9,0.9,1)
            with widget.canvas.before:
                self.color = Color(4 / 255, 30 / 255, 30 / 255, 1)  # Initial background color (white)
                rectangle = Rectangle(pos=widget.pos, size=widget.size)
            self.animation = Animation(r=33 / 255, g=76 / 255, b=65 / 255, duration=15, t='out_expo')  # Start with red background color
            self.animation += Animation(r=4 / 255, g=30 / 255, b=30 / 255, duration=10, t='out_expo')  # Transition to white background color
            self.animation.repeat = True  # Repeat the animation indefinitely
        if state:
            self.animation.start(self.color)
            self.animation.bind(on_progress=self.on_animation_progress)
        else:
            self.animation.stop(self.color)
            self.countbreaths=0

    def manipulate_size(self, scl):
        mat = Matrix().scale(scl, scl, scl)
        self.apply_transform(mat, anchor=(self.myx, self.myy), post_multiply=False)
        print("x pos ", self.myx, " y pos ", self.myy)
        self.sizex*=scl

    def on_touch_down(self, touch):
        self.isup=True
        self.myx, self.myy = touch.pos
        self.count = 0
        self.countbreaths+=1
        self.countswipe=0
        if self.countbreaths==1:
            self.animate_background_color(self.label, True)
            print("hellooooooooooo")
        # self.anim = Animation(background_color=(33 / 255, 76 / 255, 65 / 255, 1), duration=2)
        # self.anim += Animation(background_color=(4 / 255, 30 / 255, 30 / 255, 1), duration=2)
        # self.anim.repeat = True
        # self.anim.start(milayout.sct.ids.yolo)

        return super().on_touch_down(touch)


    def on_touch_move(self, touch):
        x, y = touch.pos
        self.speed = SctrLay.vect(x, y, self.myx, self.myy)
        self.myx = x
        self.myy = y
        self.count += 1
        if self.speed > 10 and self.sizex<1.0:
            self.count = 0
            self.manipulate_size(1.2)
        elif self.speed>10 and self.sizex>=1.0 and self.isup:
            rootx=milayout.size[0]
            selfx=self.pos[0]
            if selfx>(rootx/4)*3:
                self.countswipe+=1
        if self.count>350 and self.sizex>0.2:
            self.manipulate_size(0.9995)
        elif self.count>350:
            self.label2.color=(0,0,0,0)
            self.label3.color=(0,0,0,0)

        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.isup = not self.isup
        if self.count > 100 and self.sizex <= 0.2 and self.isup:
            milayout.ids.float_grid.remove_widget(self)
            milayout.fadefunc(True)
        elif self.countswipe>0 and self.isup:
            milayout.ids.float_grid.remove_widget(self)
            Clock.create_trigger(milayout.fadefunc(False))

        self.animate_background_color(self.label,False)
        return super().on_touch_up(touch)


    @staticmethod
    def vect(x, y, ox, oy):
        chngx = (x - ox) * (x - ox)
        chngy = (y - oy) * (y - oy)
        return math.sqrt(chngy + chngx)


class InfoPop(Popup):
    def __init__(self, **kwargs):
        super(InfoPop, self).__init__(**kwargs)
        self.background_button_pressed=False
        self.ids.background_button.disabled=True
        minutes, secs = divmod(milayout.totalworktime, 60)
        hours, minutes= divmod(minutes, 60)
        self.ids.total_time.text = f'{int(hours):02}:{int(minutes):02}:{int(secs):02}'

    def dismissal(self, *_args):
        global title_text
        global time_text
        title_text=self.ids.title.text
        minutes, secs=self.ids.time.text.split(":")
        time_text=f'{int(minutes):02}:{int(secs):02} '
        self.background_button_pressed=True
        self.dismiss()
        milayout.ids.l1.size_hint= (0.2,0.2)
        milayout.ids.aesth1.size_hint = (0.2, 0.2)
        milayout.ids.aesth2.size_hint = (0.2, 0.2)
        milayout.ids.aesth3.size_hint = (0.2, 0.2)
        milayout.ids.aesth4.size_hint = (0.2, 0.2)
        milayout.ids.aesth1.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        milayout.ids.aesth2.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        milayout.ids.aesth3.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        milayout.ids.aesth4.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        global sct
        global temp_lbl
        temp_lbl = SpcLabel(size_hint=(1, 1))
        sct=SctrLay()
        print('hellp')
        milayout.ids.float_grid.add_widget(temp_lbl)
        milayout.ids.float_grid.add_widget(sct)
        #milayout.write_timer()

    def thirty_buff(self, *_args):
        self.thirty_but=Label(text= "30", font_size=120, size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.fullsecs=30
        self.ids.pop_grid.add_widget(self.thirty_but)
        self.ids.background_button.disabled=False
        Clock.schedule_interval(self.thirty_timer, 0)

    def thirty_timer(self, dt):
        if self.fullsecs>1:
            self.fullsecs-=dt
        else:
            if not self.background_button_pressed:
                MDApp.get_running_app().stop()
        self.thirty_but.text=f'{int(self.fullsecs)}'




class MyLayout(Widget):

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.totalworktime=1*60
        self.isinbreak=False
        self.fullwork=0
        self.noofcycles=0
        self.fullsecs=0
        self.timeroffset=0
        # self.templabel= Label(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.templabel = temporarylabel()
        with self.templabel.canvas.before:
            Color(20 / 255, 50 / 255, 45 / 255, 1)  # Set the desired transparency (0.5 for 50%)
            self.templabel.rect = Rectangle(pos=self.templabel.pos, size=self.templabel.size)

    def ask_touch(self, dt):
        print()

    def midbreak(self):
        self.fullsecs=30
        self.fullwork=23

    def remove_temp_lbl(self, dt):
        self.ids.float_grid.remove_widget(temp_lbl)
        if self.isinbreak:
            if platform in ('macosx','macos'):
                os.system('''
                osascript -e 'tell application "System Events"' -e 'repeat 32 times' -e 'key code 107' -e 'delay 0.01' -e 'end repeat' -e 'end tell'
                osascript -e 'tell application "System Events"' -e 'repeat 3 times' -e 'key code 113' -e 'end repeat' -e 'end tell'
                ''')

    def fadefunc(self, willbebreak):
        anim=Animation(background_color=(4/255, 12/255, 9/255, 0), duration=2)
        anim.start(temp_lbl)
        if willbebreak:
            self.isinbreak=True
        else:
            self.isinbreak = False
        self.write_timer()
        Clock.schedule_once(self.remove_temp_lbl, 2.1)

    def write_timer(self):
        self.noofcycles+=1
        self.add_timers_counter = 0
        global time_text
        if not self.isinbreak:
            self.ids.l3.text=time_text
            print(time_text)
            minutes, secs=time_text.split(":")
            self.fullsecs=int(minutes)*60+int(secs)
            self.fullwork=self.fullsecs
            self.sc=0.2
            self.secfc1=0.001
            self.secfc2=0.001
            self.secfc3=0.001
            self.secfc4=0.001
            self.ids.l2.text=title_text
            #Clock.schedule_interval(self.start_timer, 1)
            self.delta_timer = 1
            self.delta_eval = self.evaluate_delta2(self.fullwork, title_text)
            self.start_timer_caller()
            Clock.schedule_interval(self.scale_lbl, 0.05)
            self.timeroffset = 0
        else:
            self.fullsecs=self.totalworktime/5
            self.full=self.fullsecs
            minutes, secs = divmod(self.fullsecs, 60)
            self.ids.l3.text = f'{int(minutes):02}:{int(secs):02} '
            self.ids.l2.text="Break"
            Clock.schedule_interval(self.start_timer, 1.1)
        print(milayout.children[0].children)

    def evaluate_delta(self, time_sec):
        fractional = 60 / time_sec
        return lambda a: -0.0000000143 * (a * fractional) ** 5 + 0.0000018835 * (a * fractional) ** 4 - 0.0000834615 * (
                    a * fractional) ** 3 + 0.001457456 * (a * fractional) ** 2 - 0.0190453792 * (
                                     a * fractional) + 1.3034044916

    def evaluate_delta2(self, time_sec, titled):
        fractional = 60 / time_sec
        if titled=='':
            return lambda a, offset: 1/(-0.0000000143 * (a * fractional) ** 5 + 0.0000018835 * (a * fractional) ** 4 - 0.0000834615 * (
                a * fractional) ** 3 + 0.001457456 * (a * fractional) ** 2 - 0.0190453792 * (
                                 a * fractional) + 1.3034044916) + offset
        else:
            return lambda a, offset: (
                        -0.0000000143 * (a * fractional) ** 5 + 0.0000018835 * (a * fractional) ** 4 - 0.0000834615 * (
                        a * fractional) ** 3 + 0.001457456 * (a * fractional) ** 2 - 0.0190453792 * (
                                a * fractional) + 1.3034044916) + offset


    def start_timer_caller(self):
        Clock.schedule_once(self.start_timer, self.delta_eval(self.delta_timer, self.timeroffset))

    def openInfo(self):
        self.ids.float_grid.remove_widget(self.ids.temp)

    def start_timer(self, dt):
        add_timers_list = [2, 5, 7, 10]
        global title_text
        global time_text
        # print(dt)
        if self.fullsecs>1:
            self.fullsecs-=1
            minutes, seconds = divmod(self.fullsecs, 60)
            if self.fullsecs > 59:
                self.ids.l3.text = f'{int(minutes):02}:{int(seconds):02}'
                self.ids.l3.font_size =60
                self.ids.l3.pos_hint = {"center_x": 0.5, "center_y": 0.45}

            else:
                # from plyer import notification
                # if 59 <= self.fullsecs <= 60:
                #     notification.notify(
                #         app_name="Rect",
                #         title="1 min remaining",
                #         timeout=2,
                #     )
                if 59 <= self.fullsecs <= 60:
                    self.delta_timer = 1
                    self.timeroffset = 0
                    if title_text != '' and self.noofcycles>1:
                        self.fullsecs += add_timers_list[self.add_timers_counter]*60 if self.add_timers_counter<4 else add_timers_list[3]*60
                        self.add_timers_counter += 1
                        print(self.add_timers_counter)
                        self.show_notification("Rect", f"{add_timers_list[self.add_timers_counter] if self.add_timers_counter<4 else add_timers_list[3]} min added")
                    else:
                        self.show_notification("Rect", "1 min remaining")

                self.ids.l3.text = str(int(seconds))
                self.ids.l3.font_size = 120
                self.ids.l3.pos_hint = {"center_x": 0.5, "center_y": 0.5}
                self.ids.l2.text = ""
            if not self.isinbreak:
                Clock.unschedule(self.start_timer)
                self.delta_timer += 1
                self.start_timer_caller()
        else:
            self.fullsecs=0
            Clock.unschedule(self.start_timer)
            Clock.unschedule(self.scale_lbl)
            if not self.isinbreak:
                self.totalworktime += self.fullwork
                # notification.notify(
                #     app_name="Rect",
                #     title="Your work session is over",
                #     timeout=2,
                # )
                self.show_notification("Rect", "Your work session is over")
                if self.noofcycles==1:
                    title_text="Speed"
                    time_text="03:00"
                    global sct
                    global temp_lbl
                    temp_lbl = SpcLabel(size_hint=(1, 1))
                    sct = SctrLay()
                    self.ids.float_grid.add_widget(temp_lbl)
                    self.ids.float_grid.add_widget(sct)
                    self.ids.l1.size_hint = (0.2, 0.2)
                    self.ids.aesth1.size_hint = (0.2, 0.2)
                    self.ids.aesth2.size_hint = (0.2, 0.2)
                    self.ids.aesth3.size_hint = (0.2, 0.2)
                    self.ids.aesth4.size_hint = (0.2, 0.2)
                    self.ids.aesth1.pos_hint = {"center_x":0.5, "center_y":0.5}
                    self.ids.aesth2.pos_hint = {"center_x":0.5, "center_y":0.5}
                    self.ids.aesth3.pos_hint = {"center_x":0.5, "center_y":0.5}
                    self.ids.aesth4.pos_hint = {"center_x":0.5, "center_y":0.5}

                else:
                    Factory.InfoPop().open()
            else:
                # notification.notify(
                #     app_name="Rect",
                #     title="Work's about to start",
                #     timeout=2,
                # )

                self.show_notification("Rect", "Work's about to start")
                self.totalworktime=0
                self.isinbreak=False
                self.write_timer()


    def scale_lbl(self, dt):
        self.vect_count=0
        fc=0.85/(self.fullwork/0.05)
        self.sc +=fc
        self.secfc1 += fc*0.225
        self.secfc2 += fc*0.225*2
        self.secfc3 += fc*0.225*4
        self.secfc4 += fc*0.225*8
        self.ids.l1.size_hint = self.sc, self.sc
        bbox1=self.sc +self.secfc1
        bbox2=self.sc + self.secfc1 + self.secfc2
        bbox3=self.sc + self.secfc1 + self.secfc2 + self.secfc3
        bbox4= self.sc + self.secfc1 + self.secfc2 + self.secfc3 + self.secfc4
        self.ids.aesth1.size_hint = bbox1, bbox1
        self.move_lbl(self.ids.aesth1)
        self.ids.aesth2.size_hint = bbox2, bbox2
        self.move_lbl(self.ids.aesth2)
        self.ids.aesth3.size_hint = bbox3, bbox3
        self.move_lbl(self.ids.aesth3)
        self.ids.aesth4.size_hint = bbox4, bbox4
        self.move_lbl(self.ids.aesth4)

    def move_lbl(self, lbl):
        vect = (0.8 / (self.fullwork / 0.05)) * 1.5 * lbl.size_hint[0]
        bound = (0.5 - 0.15 * lbl.size_hint[0], 0.5 + 0.15 * lbl.size_hint[0])
        if lbl.pos_hint["center_x"]<=bound[0] or lbl.pos_hint["center_x"]>=bound[1]:
            lbl.change_dir('x')
        elif lbl.pos_hint["center_y"]<=bound[0] or lbl.pos_hint["center_y"]>=bound[1]:
            lbl.change_dir('y')
        else:
            lbl.pos_hint["center_x"] += lbl.val_x * vect
            lbl.pos_hint["center_y"] += lbl.val_y * vect

    def on_touch_down(self, touch):
        if self.ids.thisfloat.collide_point(*touch.pos):
            anim = Animation(pos_hint={"center_x": -0.1}, duration=1, t='out_quad')
            anim.start(self.ids.bob)
            print("hello")
        super().on_touch_down(touch)
        # # Clock.schedule_once(self.animate_pane_open, 0.5)
        # anim = Animation(pos_hint={"center_x": 0.1}, duration=1, t='out_quad')
        # # anim = Animation(background_color=(4 / 255, 12 / 255, 9 / 255, 0), duration=2)
        # anim.start(self)
        # print("hello000")
        # self.toggle=not self.toggle

    def add_task(self):
        self.entrywidg=ObjEntry()
        self.ids.thisfloat.add_widget(self.entrywidg)

    def del_task(self):
        self.ids.thisfloat.remove_widget(self.entrywidg)

    def show_notification(self, title, message):
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title)
        notification.setInformativeText_(message)
        notification.setSoundName_(NSUserNotificationDefaultSoundName)

        center = NSUserNotificationCenter.defaultUserNotificationCenter()
        center.deliverNotification_(notification)


class temporarylabel(Label):
    pass


class NewApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_diff=0
        # self.templabel = Label(size_hint=(1, 1), pos_hint={'center_x':0.5, 'center_y':0.5})
        # with self.templabel.canvas.before:
        #     Color(20 / 255, 50 / 255, 45 / 255, 1)  # Set the desired transparency (0.5 for 50%)
        #     self.templabel.rect = Rectangle(pos=self.templabel.pos, size=self.templabel.size)
        # self.templabel=temporarylabel()

    def set_window_level(self, dt):
        # Get a reference to the application instance
        app = NSApplication.sharedApplication()

        # Get the main window of your application
        window = app.windows()[0]  # Assuming there is at least one window

        # Set the window level to floating
        window.setLevel_(NSFloatingWindowLevel)

        # Activate the application (optional)
        app.activateIgnoringOtherApps_(True)

    def build(self):
        os.system('''
        autohide_value=$(defaults read com.apple.dock autohide)
        if [[ $autohide_value == "0" ]]; then
          defaults write com.apple.dock autohide -bool true
          killall Dock
        fi
        ''')
        Window.minimum_width  = 450
        Window.minimum_height = 300
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.mouse_count=0
        self.currtime=0
        global milayout
        milayout = MyLayout()
        Clock.schedule_once(self.set_window_level, 0.1)
        self.listofclicks=[]
        Window.bind(on_cursor_enter=lambda a: self.count_mouses( True))
        Window.bind(on_cursor_leave=lambda a: self.count_mouses( False))
        return milayout

    def count_mouses(self, state):
        Clock.unschedule(self.start_time_diff)
        if milayout.templabel.parent is not None:
            milayout.ids.float_grid.remove_widget(milayout.templabel)
        if milayout.fullsecs>0 and not milayout.isinbreak:
            diff=0
            if state:
                self.currtime=time.time()
                self.listofclicks.append(int(self.betweenclicks+0.5))
                if len(self.listofclicks)>5:
                    self.listofclicks.pop(0)
                print(milayout.timeroffset)
            else:
                diff=time.time()-self.currtime
                self.currtime = time.time()
                self.betweenclicks=0
                Clock.schedule_interval(self.start_time_diff, 0)
                if diff>0.5:
                    self.mouse_count += 1
                else:
                    self.listofclicks.pop()
                if self.listofclicks!=[]:
                    self.med = statistics.mean(self.listofclicks)
                    print(self.med, 'median datapoint', self.mouse_count)
                    if self.listofclicks[-1]-self.med > self.med/5:
                        if title_text != '':
                            milayout.timeroffset -= 0.15
                        else:
                            milayout.timeroffset += 0.15
                    elif self.med-self.listofclicks[-1] > self.med/5:
                        if title_text != '':
                            milayout.timeroffset += 0.15
                        else:
                            milayout.timeroffset -= 0.15
        else:
            self.mouse_count=0
            self.betweenclicks=0

    def start_time_diff(self, df):
        if time.time()-self.currtime>15:
            if milayout.templabel.parent is None:
                milayout.ids.float_grid.add_widget(milayout.templabel)
        elif milayout.templabel.parent is not None:
            milayout.ids.float_grid.remove_widget(milayout.templabel)
        self.betweenclicks+=df



    def on_window_resize(self, instance, size):
        # Define the maximum width and height
        max_width = 450
        max_height = 300

        # Check if the window size exceeds the maximum
        if size[0] > max_width or size[1] > max_height:
            Window.size = (min(size[0], max_width), min(size[1], max_height))



if __name__ == "__main__":
    Window.fullscreen = False
    NewApp().run()

