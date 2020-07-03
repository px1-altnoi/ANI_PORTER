import maya.cmds as cmds

import os
import json

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'AnimLib')
ANIM_NAME = "untitled"


def createDirectory(directory=DIRECTORY):
    if not os.path.exists(directory):
        os.mkdir(directory)


class AniPorterLibrary(dict):
    def save(self, name, start, end, directory=DIRECTORY, **info):
        createDirectory(directory)

        jsonfile = os.path.join(directory, '%s.json' % name)

        items = cmds.ls(selection=True)

        Done_list = []
        tops = {}
        for item in items:
            keyitems = cmds.keyframe(item, q=True, name=True)
            if keyitems is not None:
                for keyitem in keyitems:
                    if keyitem not in Done_list:
                        Done_list.append(keyitem)
                        count = cmds.keyframe(keyitem, q=True, kc=True)
                        elements = {}

                        for i in range(0, count - 1):
                            val = cmds.keyframe(keyitem, index=(i, i), vc=True, q=True)
                            time = cmds.keyframe(keyitem, index=(i, i), tc=True, q=True)
                            cval = 0
                            ctime = 0
                            for temp in val:
                                cval = temp
                            for temp in time:
                                ctime = temp
                            if start <= ctime <= end:
                                elements[i] = {"time": ctime, "value": cval}
                        tops[keyitem] = elements
            JSON_BASE = tops

            with open(jsonfile, 'w') as f:
                json.dump(JSON_BASE, f, indent=4)

            self[jsonfile] = os.path.join(directory, jsonfile)

    def load(self, name, directory=DIRECTORY):
        jsonfile = os.path.join(directory, '%s' % name)
        with open(jsonfile, 'r') as f:
            payload = json.load(f)
            keylist = payload.keys()
            for key in keylist:
                list = [int(n) for n in payload[key].keys()]
                list.sort()
                for i in list:
                    cmds.currentTime(payload[key][str(i)]["time"], e=True, update=False)
                    objName, tgt = key.rsplit('_', 1)
                    cmds.select(clear=True)
                    cmds.select(objName)
                    cmds.setKeyframe(v=payload[key][str(i)]["value"], at=tgt)

    def find(self, directory=DIRECTORY):
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        jsonfiles = [f for f in files if f.endswith('.json')]

        for jsonfile in jsonfiles:
            self[jsonfile] = os.path.join(directory, jsonfile)