import torch.utils.data as data

from PIL import Image
import os
import os.path

def default_loader(path):
    img = Image.open(path).convert('L')
    return img

def default_list_reader(fileList):
    imgList = []
    print(fileList)
    with open(fileList, 'r') as file:
        for line in file.readlines():
            imgPath, label = line.strip().split(' ')
            imgList.append((imgPath, int(label)))
    return imgList

def default_attr_reader(attrlist):
    attr = {}
    for attrfile in attrlist:
        with open(attrfile, 'r') as file:
            # line 1 is the number of pic
            number = file.readline()
            # line 2 are attr names
            attrname = file.readline().strip().split(' ')
            # the rest are val
            for line in file.readlines():
                val = line.strip().split()
                pic_name = val[0]
                val.pop(0)
                img_attr = {}
                if pic_name in attr:
                    img_attr = attr[pic_name]

                for i,name in enumerate(attrname,0):
                    img_attr[name] = int(val[i]) # maybe can store as str. do not use int

                attr[pic_name] = img_attr
    return attr

class ImageList(data.Dataset):
    def __init__(self, root, fileList, attrlist = [], transform=None, list_reader=default_list_reader, attr_reader = default_attr_reader, loader=default_loader):
        # for celeba root is /data/..../celeba/img_....
        # for celeba filelist is /data/...../celeba/Anno/identi....
        # for celeba attrlist is [/data/...../celeba/Anno/xxx.txt, ..../xxx.txt]
        self.root      = root
        self.imgList   = list_reader(fileList)
        self.transform = transform
        self.loader    = loader
        self.attr      = attr_reader(attrlist)

    def __getitem__(self, index):
        imgPath, target = self.imgList[index]
        img = self.loader(os.path.join(self.root, imgPath))
        img_attr = self.attr[imgPath]
        if self.transform is not None:
            img = self.transform(img)
        return img, target, img_attr

    def __test__(self,index):
        imgPath, target = self.imgList[index]
        img_attr = self.attr[imgPath]
        return imgPath, target, img_attr
    def __len__(self):
        return len(self.imgList)
