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

        project = lambda p: (P @ (np.dot(M, np.dot(T, p).T)))
        devide = lambda p: p/p[3]
        n_points = np.array([project(pi) for pi in n_points])
        n_points = np.array([devide(pi) for pi in n_points])
        n_points[:,0] = ((n_points[:,0] + 1) * 0.5 * self.SCREEN_W)
        n_points[:,1] = ((1 - (n_points[:,1] + 1) * 0.5) * self.SCREEN_H)
        n_points = n_points.squeeze()

        #for i in range(len(n_points)):
        #    tmp = np.dot(M, np.dot(T, n_points[i]).T)
        #    tmp = (P @ tmp)

        #    if tmp[3] != 1:
        #        tmp = tmp/tmp[3]

        #    tmp[0] = ((tmp[0] + 1) * 0.5 * self.SCREEN_W)
        #    tmp[1] = ((1 - (tmp[1] + 1) * 0.5) * self.SCREEN_H)
        #    n_points[i] = tmp.T

        return n_points

    def calculate_triangle_depth(self, points, triangle):
        # Get the vertices for each triangle
        v1, v2, v3 = points[triangle]
        # Compute average z-depth
        avg_depth = (v1[2] + v2[2] + v3[2]) / 3.0
        return avg_depth

    def sort_triangles_by_depth(self, points, triangles, shade):
        light_dir = np.asarray([np.sin(pygame.time.get_ticks()/1000), 1, 1])
        light_dir = light_dir/np.linalg.norm(light_dir)

        depths = []
        for i in range(len(triangles)):
            triangle = triangles[i]
            # Use Cross-Product to get surface normal
            vet1 = points[triangle[1]][:3]  - points[triangle[2]][:3]
            vet2 = points[triangle[0]][:3] - points[triangle[2]][:3]

            # backface culling with dot product between normal and camera ray
            normal = np.cross(vet2, vet1)
            normal = normal/np.sqrt(normal[0]*normal[0] + normal[1]*normal[1] + normal[2]*normal[2])
            shade[i] = 0.5*self.dot_3d(light_dir, normal) + 0.5


            # Calculate the depth of each triangle and store it with the triangle
            depths.append((self.calculate_triangle_depth(points, triangle), i))
        
        # Sort triangles by depth (from back to front)
        sorted_triangles = sorted(depths, key=lambda x: x[0], reverse=False)
        # Extract sorted triangles
        #sorted_triangles = [triangle for _, triangle in sorted_triangles]
        #print(sorted_triangles)
        return sorted_triangles

    def dot_3d(self, arr1, arr2):
        return arr1[0]*arr2[0] + arr1[1]*arr2[1] + arr1[2]*arr2[2]

    def sort_triangles(self, points, screen_points, triangles, camera, z_order, shade):
        light_dir = np.asarray([np.sin(pygame.time.get_ticks()/1000), 1, 1])
        light_dir = light_dir/np.linalg.norm(light_dir)

        for i in range(len(triangles)):
            triangle = triangles[i]

            # Use Cross-Product to get surface normal
            vet1 = points[triangle[1]][:3]  - points[triangle[2]][:3]
            vet2 = points[triangle[0]][:3] - points[triangle[2]][:3]

            # backface culling with dot product between normal and camera ray
            normal = np.cross(vet2, vet1)
            normal = normal/np.sqrt(normal[0]*normal[0] + normal[1]*normal[1] + normal[2]*normal[2])

            CameraRay = points[triangle[0]][:3] - camera.pos
            dist2cam = np.sqrt(CameraRay[0]*CameraRay[0] + CameraRay[1]*CameraRay[1] + CameraRay[2]*CameraRay[2])
            CameraRay = CameraRay/dist2cam

            # get projected 2d points for filtering of offscreen triangles
            xxs = np.asarray([screen_points[triangle[0]][0:2][0],  screen_points[triangle[1]][0:2][0],  screen_points[triangle[2]][0:2][0]])
            yys = np.asarray([screen_points[triangle[0]][0:2][1],  screen_points[triangle[1]][0:2][1],  screen_points[triangle[2]][0:2][1]])

            # check valid values
            if (self.dot_3d(normal, CameraRay) < 0 and 
                np.min(xxs) > - self.SCREEN_W and 
                np.max(xxs) < 2*self.SCREEN_W and 
                np.min(yys) > - self.SCREEN_H and 
                np.max(yys) < 2*self.SCREEN_H):

                z_order[i] = -dist2cam

                # calculate shading, normalize, dot and to 0 - 1 range
                shade[i] = 0.5*self.dot_3d(light_dir, normal) + 0.5

            # big value for last positions in sort
            else: z_order[i] = 9999

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


        import time
        for obj in world.objects:
            start = time.time()
            points = self.point2screen(P_view, R_view, T_view, obj.points)
            end = time.time()
            length = end - start
            #print("1 took", length, "seconds!")

            triangles = obj.triangles

            z_order = np.zeros(len(triangles))
            shade = z_order.copy()
            start = time.time()
            #self.sort_triangles(obj.points, points, triangles, world.camera, z_order, shade)
            sorted_t = self.sort_triangles_by_depth(points, triangles, shade)
            end = time.time()
            length = end - start
            #print("2 took", length, "seconds!")

            color_scale = 230/np.max(np.abs(points))

            #for index in range(len(triangles)):
            #for index in np.argsort(z_order):
            for d, index in sorted_t:
                #if z_order[index] == 9999: break
                tmp = [points[triangles[index][0]][0:2], points[triangles[index][1]][0:2], points[triangles[index][2]][0:2]]
                color = [100, 35, 98] / abs(d)
                color = shade[index]*np.abs(points[triangles[index][0]][:3])*color_scale +25
                #color = np.abs(points[triangles[index][0]][:3])*45 +25
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

