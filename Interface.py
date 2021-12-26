# Creating the interface
import random
from tkinter import Tk, Canvas


WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


# Класс сегмента змейки, один ее кусок, будет использоваться для конструирования змеи
class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="white")


class Snake(object):
    def __init__(self, segments):
        self.segments = segments

        # Список направлений, куда может ползти змейка
        # ??? Не совсем уверен, что такой стиль оформления словарей по Pep, но моему глазу так нравится
        # ??? Если знаешь, как по науке делается, поправь, я гляну
        self.mapping = {
                        "Down": (0, 1),
                        "Up": (0, -1),
                        "Left": (-1, 0),
                        "Right": (0, -1)
                        }

        self.vector = self.mapping["Right"]

    def move(self):
        """Метод, определяющий движение змеи"""
        # ??? Насколько я понял, присваивает каждому текущему сегменту позицию следующего
        for segment in range(len(self.segments) - 1):
            current_segment = self.segments[segment].instance
            x1, y1, x2, y2 = c.coords(self.segments[segment+1].instance)
            c.coords(current_segment, x1, y1, x2, y2)

        # ??? Вроде в методе выше мы математически задали перемещение змеи, а здесь переносим его
        # ??? графически на объект Canvas
        c.coords(self.segments[-1].instance,
                x1 + self.vector[0]*SEG_SIZE,
                y1 + self.vector[1] * SEG_SIZE,
                x2 + self.vector[0] * SEG_SIZE,
                y2 + self.vector[1] * SEG_SIZE
                )

    def change_direction(self, event):
        """Поворот головы змейки"""
        #??? пока не знаю что такое event keysym, кажись че-то встроенное в питон/ткинкер
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        """Добавление элемента змейки, после того, как она съест еду"""

        last_seg = c.coords(self.segments[0].instance)

        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE

        self.segments.insert(0, Segment(x, y))


def create_apple():
    """ Создает яблоко в случайной позиции на карте """
    global APPLE
    posx = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
    posy = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))

    APPLE = c.create_oval(posx, posy,
                          posx + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill="red")


def main():
    global IN_GAME

    if IN_GAME:
        # Двигаем змейку
        s.move()

        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # Столкновение с границами экрана
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # Поедание яблок
        elif head_coords == c.coords(APPLE):
            s.add_segment()
            c.delete(APPLE)
            create_apple()

        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(s.segments) - 1):
                if c.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False

    # Если не в игре выводим сообщение о проигрыше
    else:
        c.create_text(WIDTH / 2, HEIGHT / 2,
                      text="GAME OVER!",
                      font="Arial 20",
                      fill="#ff0000")


def create_snake():
    segments = [
        Segment(SEG_SIZE, SEG_SIZE),
        Segment(SEG_SIZE * 2, SEG_SIZE),
        Segment(SEG_SIZE * 3, SEG_SIZE),
    ]
    return Snake(segments)


def start_game():
    global s
    create_apple()
    s = create_snake()
    c.bind("<KeyPress>", s.change_direction)
    main()


window = Tk()
window.title("KrasNIPI in collaboration with GPN snake game for $1000000000")

c = Canvas(window, width=WIDTH, height=HEIGHT, bg="#555555")
c.grid()
c.focus_set()

start_game()
window.mainloop()