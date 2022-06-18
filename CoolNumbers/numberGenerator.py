
import math

from PIL import Image
from os.path import join

def getImage(number,number2,path = ""):

    def GIFtoARRAY(gif):
        images = []
        for frame in range(0, gif.n_frames):
            gif.seek(frame)
            new_image = Image.new('RGBA', (gif.size[0], gif.size[1]))
            new_image.paste(gif, (0, 0))
            images.append(new_image)
        return images


    ims = [GIFtoARRAY(Image.open(join(path,join("numbers",i+".gif")))) for i in str(number)]


    def combine(im1,im2):
        l1 = len(im1)
        l2 = len(im2)

        lcm = min(l1,l2)
        images = []

        for frame in range(0, lcm):
            new_image = Image.new('RGBA', (im1[frame%l1].size[0]+im2[frame%l2].size[0], im1[frame%l1].size[1]))
            new_image.paste(im1[frame%l1], (0, 0))
            new_image.paste(im2[frame%l2], (im1[frame%l1].size[0], 0))
            images.append(new_image)

        return images

    imn = ims[0]
    for i in range(1,len(ims)):
        imn = combine(imn,ims[i])

    ims = [GIFtoARRAY(Image.open(join(path,join("numbers",i+".gif")))) for i in str(number2)]
    imn = combine(imn, GIFtoARRAY(Image.open(join(path,"numbers\\e2.gif"))))

    for i in range(len(ims)):
        imn = combine(imn,ims[i])

    return imn

if __name__ == "__main__":
    frames = getImage(2387645823765482387263548762538476765872364587236548726354876235487623548723654827364582736548723645,237645723654238746523876452387645823764582234)
    frames[0].save('pillow_imagedraw.gif', save_all=True, append_images=frames[1:], optimize=False, duration=160,loop=0, transparency=0, disposal=2)










