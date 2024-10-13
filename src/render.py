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
        self.SCREEN_W = abs(viewport[1][0] - viewport[0][0])
        self.SCREEN_H = abs(viewport[1][1] - viewport[0][1])
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

    def point2screen(self, P, M, T, points):
        n_points = np.matrix.copy(points)

        for i in range(len(n_points)):
            tmp = np.dot(M, np.dot(T, n_points[i]).T)
            tmp = (P @ tmp)

            if tmp[3] != 1:
                tmp = tmp/tmp[3]

            tmp[0] = ((tmp[0] + 1) * 0.5 * self.SCREEN_W)
            tmp[1] = ((1 - (tmp[1] + 1) * 0.5) * self.SCREEN_H)
            n_points[i] = tmp.T

        return n_points

    def update(self, world):
        self.screen.fill((40, 40, 40))

        # adjust camera
        if world.mode == "game":
            pass

        # draw
        x, y, z = world.camera.pos
        pitch = world.camera.pitch
        yaw = world.camera.yaw

        xzLen = np.cos(pitch)
        xld = xzLen * np.cos(yaw)
        zld = np.sin(pitch)
        yld = xzLen * np.sin(-yaw)

        xzLen = np.cos(pitch + np.pi/2)
        xup = xzLen * np.cos(yaw)
        zup = np.sin(pitch + np.pi/2)
        yup = xzLen * np.sin(-yaw)

        e = np.array([x, y, z, 1])

        g = np.array([xld, yld, zld])
        g = g / np.linalg.norm(g)

        t = np.array([xup, yup, zup])
        t = t / np.linalg.norm(t)

        gt = np.cross(g, t)
        gt = gt / np.linalg.norm(gt)

        g = np.array([g[0], g[1], g[2], 1])
        t = np.array([t[0], t[1], t[2], 1])

        T_view = np.matrix([
            [1, 0, 0, -e[0]],
            [0, 1, 0, -e[1]],
            [0, 0, 1, -e[2]],
            [0, 0, 0, 1],
        ])

        R_view = np.matrix([
            [gt[0], gt[1], gt[2], 0],
            [t[0], t[1], t[2], 0],
            [-g[0], -g[1], -g[2], 0],
            [0, 0, 0, 1],
        ])

        zNear = -0.1
        zFar = -50
        fovy = np.deg2rad(90) #eye_fov
        P_view = np.zeros((4,4))

        top = np.tan(fovy/2) * abs(zNear)
        bottom = - top
        right = (self.SCREEN_W / self.SCREEN_H) * top
        left = -right

        P_view[0][0] = zNear / (right)
        P_view[0][3] = 0
        P_view[1][1] = zNear / (top)
        P_view[1][3] = 0
        P_view[2][2] = (zNear + zFar)/(zNear - zFar);
        P_view[2][3] = -2 * (zNear * zFar)/(zNear - zFar);
        P_view[3][2] = 1;
        P_view[3][3] = 0;

        #some ui
        pygame.draw.line(self.screen, (150, 0, 0), (0.9 * self.SCREEN_W, 0.1 * self.SCREEN_H), (0.9 * self.SCREEN_W, 0.1 * self.SCREEN_H - 15))
        pygame.draw.line(self.screen, (0, 150, 0), (0.9 * self.SCREEN_W, 0.1 * self.SCREEN_H), (0.9 * self.SCREEN_W - 15 * np.cos(yaw - np.pi/2), 0.1 * self.SCREEN_H + 15 * np.sin(yaw - np.pi/2)))
        pygame.draw.line(self.screen, (150, 0, 0), (0.95 * self.SCREEN_W, 0.1 * self.SCREEN_H), (0.95 * self.SCREEN_W + 15, 0.1 * self.SCREEN_H))
        pygame.draw.line(self.screen, (0, 150, 0), (0.95 * self.SCREEN_W, 0.1 * self.SCREEN_H), (0.95 * self.SCREEN_W + 15 * np.cos(pitch), 0.1 * self.SCREEN_H - 15 * np.sin(pitch)))
        myFont = pygame.font.SysFont("Times New Roman", 18)
        pos_display = myFont.render(str((round(float(x), 2), round(float(y), 2), round(float(z), 2))), 1, (255, 255, 255))
        self.screen.blit(pos_display, (520, 30))

        for obj in world.objects:
            points = self.point2screen(P_view, R_view, T_view, obj.points)
            triangles = obj.triangles
            for index in range(len(triangles)):
                tmp = [points[triangles[index][0]][0:2], points[triangles[index][1]][0:2], points[triangles[index][2]][0:2]]
                print(tmp)
                color = [100, 35, 98]
                pygame.draw.polygon(self.screen, color, tmp)

        #for obj in world.objects:
        #    points = self.project_points(obj.points, world.camera)
        #    triangles = obj.triangles
        #    #color_scale = 230/np.max(np.abs(points))
        #    for index in range(len(triangles)):
        #        tmp = [points[triangles[index][0]][3:], points[triangles[index][1]][3:], points[triangles[index][2]][3:]]
        #        color = [100, 35, 98]
        #        #color = np.abs(points[triangles[index][0]][:3])*45 +25
        #        pygame.draw.polygon(self.screen, color, tmp)

