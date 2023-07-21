from deep_sort_realtime.deepsort_tracker import DeepSort 


class Product_tracker():
    TRACKER = DeepSort(max_age=2)
    __cur_det = dict()
    __prev_det = dict()
    __boughted_products = list()

    def track_face(self, bboxes, frame):
        tracks = self.TRACKER.update_tracks(bboxes, frame=frame)

        self.__cur_det={}

        for track in tracks:
            if not track.is_confirmed():
                continue
            self.__cur_det[track.track_id] = track.det_class
    
    def check_ids(self):
        #=================================================== проверка текущих детекций
        need_delete =[]
        for prev in self.__prev_det:
            if prev not in self.__cur_det:
                self.__boughted_products.append(self.__prev_det[prev])
                need_delete.append(prev)

        for n in need_delete:
            self.__prev_det.pop(n, None)

        for cur in self.__cur_det:
            if cur not in self.__prev_det:
                self.__prev_det[cur] = self.__cur_det[cur]
                if self.__prev_det[cur] in self.__boughted_products:
                    self.__boughted_products.remove(self.__prev_det[cur])
                

    def run_shelf_monitoring(self, frame, detections):
        bbs = []

        for d in detections:
            ltrb = [d['xmin'],d['ymin'], (d['xmax']-d['xmin']), (d['ymax']-d['ymin'])]
            bbs.append([ltrb, d['confidence'],d['name']])

        self.track_face(bbs, frame)
        self.check_ids()

        print(self.__boughted_products)
        print()