# !/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Zhiquan Wang'
__date__ = '2018/7/20 22:08'

import json
from taginfo import *
from pfgrid import *


class PixelMap(object):
    def __init__(self, *, map_height=0, map_width=0, json_info=None):
        if json_info is None:
            self.__height = map_height
            self.__width = map_width
            self.__grid_map = [[PixelGrid()] * self.__width for i in range(self.__height)]
        else:
            self.parse_json(json_info)

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def grid_map(self):
        return self.__grid_map

    def set_grid(self, _vec, _grid):
        self.__grid_map[_vec[0]][_vec[1]] = _grid

    def __dict__(self):
        return {JsonAttribute.pfm_height: self.__height,
                JsonAttribute.pfm_width: self.__width,
                JsonAttribute.pfm_grid_map: [[self.__grid_map[x][y].__dict__ for x in range(self.__width)] for y in
                                             range(self.__height)]}

    def dump_json(self):
        return json.dumps(self.__dict__())

    def parse_json(self, _s):
        tmp_dict = json.loads(_s)
        self.__height = tmp_dict[JsonAttribute.pfm_height]
        self.__width = tmp_dict[JsonAttribute.pfm_width]
        tmp_map_list = tmp_dict[JsonAttribute.pfm_grid_map]
        for x in range(self.__width):
            for y in range(self.__height):
                tmp_grid_dict = tmp_map_list[x][y]
                tmp_grid = PixelGrid(tmp_grid_dict[JsonAttribute.pfg_type],
                                     tmp_grid_dict[JsonAttribute.pfg_attribution],
                                     tmp_grid_dict[JsonAttribute.pfg_value])
                self.__grid_map[x][y] = tmp_grid
