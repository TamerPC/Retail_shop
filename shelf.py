class Shelf():
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0
    __space = []

    def __init__(self, pos_x_min=0, pos_y_min=0, pos_x_max=0, pos_y_max=0):
        self.x_min = pos_x_min
        self.y_min = pos_y_min
        self.x_max = pos_x_max
        self.y_max = pos_y_max

    def check_products(self, detections):
        self.__space = []
        for d in detections:
            mid_x, mid_y = self.find_center(d['xmin'], d['xmax'], d['ymin'], d['ymax'])
            if self.check_hit(mid_x, mid_y):
                self.__space.append(d['name']) #or class
        return self.__space

    def find_center(self, x_min, x_max, y_min, y_max):
        return (x_min+x_max)/2, (y_min+y_max)/2
    
    def check_hit(self, x, y):
        if x >= self.x_min and x <= self.x_max and y >= self.y_min and y <= self.y_max:
            return True
        else:
            return False