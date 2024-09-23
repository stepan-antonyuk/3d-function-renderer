import pygame
import numpy as np
import math
from coords import CoordConverter


class Renderer:

    def __init__(self, screen, viewport, scale):
        self.coords = CoordConverter(scale, viewport)
        self.screen = screen
        self.viewport = viewport
        self.scale = scale
        self.speed = 5
        self.color = (250,0,0)  # (250,250,250) and (0,0,0)
        self.line_thickness = 5
        self.MAX_DEPTH = 1000
        self.SCREEN_W = 1000
        self.SCREEN_H = 1000
        self.FOV_Y = np.pi/4
        self.FOV_X = self.FOV_Y * self.SCREEN_W / self.SCREEN_H

    def set_scale(self, new_scale):
        self.scale = new_scale
        self.coords = CoordConverter(self.scale, self.viewport)

    def add_scale(self, d_scale):
        new_scale = (self.scale[0] + d_scale[0], self.scale[1] + d_scale[1])
        self.scale = new_scale
        self.coords = CoordConverter(self.scale, self.viewport)

    def project_points(self, points, camera):
        camera_pos = camera.pos
        n_points = points

        for point in n_points:
            h_angle_camera_point = np.arctan((point[2]-camera_pos[2])/(point[0]-camera_pos[0] + 1e-16))

            if abs(camera_pos[0]+np.cos(h_angle_camera_point)-point[0]) > abs(camera_pos[0]-point[0]):
                h_angle_camera_point = (h_angle_camera_point - np.pi)%(2*np.pi)

            h_angle = (h_angle_camera_point-camera.yaw)%(2*np.pi)

            if h_angle > np.pi: h_angle =  h_angle - 2*np.pi

            point[3] = self.SCREEN_W*h_angle/self.FOV_X + self.SCREEN_W/2

            distance = np.sqrt((point[0]-camera_pos[0])**2 + (point[1]-camera_pos[1])**2 + (point[2]-camera_pos[2])**2)

            v_angle_camera_point = np.arcsin((camera_pos[1]-point[1])/distance)
            
            v_angle = (v_angle_camera_point - camera.pitch)%(2*np.pi)
            if v_angle > np.pi: v_angle =  v_angle - 2*np.pi
            
            point[4] = self.SCREEN_H*v_angle/self.FOV_Y + self.SCREEN_H/2

        return n_points

    def update(self, world):
        self.screen.fill((40, 40, 40))

        # adjust camera
        if world.mode == "game":
            pass

        # draw
        #x, y, z = world.camera.pos
        #pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 5, 0)

        #x, y, z = world.camera.pos
        #e = np.array([x, y, z, 1])
        #x, y, z = world.camera.lookdir
        #g = np.array([x, y, z])
        #x, y, z = world.camera.updir
        #t = np.array([x, y, z])

        #gt = np.cross(g, t)

        #T_view = np.matrix([
        #    [1, 0, 0, -e[0]],
        #    [0, 1, 0, -e[1]],
        #    [0, 0, 1, -e[2]],
        #    [0, 0, 0, 1],
        #])

        #R_view = np.matrix([
        #    [gt[0], gt[1], gt[2], 0],
        #    [t[0], t[1], t[2], 0],
        #    [g[0], g[1], g[2], 0],
        #    [0, 0, 0, 1],
        #])

        #print(T_view)
        #print(R_view)
        #tmp = np.dot(T_view, e.T)
        #tmp = np.dot(R_view, tmp.T)
        #print( tmp)

        for obj in world.objects:
            for triangle in obj.shape:
                points = self.project_points(triangle.points, world.camera)
                trgl = triangle.triangles
                for index in range(len(trgl)):
                    tmp = [points[trgl[index][0]][3:], points[trgl[index][1]][3:], points[trgl[index][2]][3:]]
                    color = [100, 35, 98]
                    pygame.draw.polygon(self.screen, color, tmp)
                
                    




