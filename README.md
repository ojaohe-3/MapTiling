# MapTiling


This project was to explore the possiblity of using AI to detect farmland and generate a polygon that fills in the farm.
Unfortunatly i ran out of time, and only completed the generation of data, that does not work fully as intentional. Likley due to how i generate the data, in some form of translation error that i have no time fixing.

## AI Model (proposed only, some light code exist)


## Data generation
I had a json, called  trainingDataFields, in it contained all geojson objects, this was then trasnlated on to map tiles, using tilenames as shown in [this method:](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers) then it was mapped to images generated by [MapBox](https://www.mapbox.com/).
### Poly
Helper class, that can convert lat, lon to its respective tiles and vice versa.

```py
def generate_polygon():
    """
    Generates polygons of sweden.
    Generates a polygon of each iland.
    e.g. gotland and mainland

    """
 
def xtile(lon):
    return int(n * ((lon+180)/360))

def ytile(lat):
    rad = np.deg2rad(lat)
    return int(n * (1-np.log(np.tan(rad) + (1/np.cos(rad)))/np.pi)/2)

def getPixel(lon, lat, size):
    # find the unit vector of lon/lan then project up to img size, this is naive, because lon, lat is not euclidian, but this is accurate enough

def num2deg(x, y):
 # given x tile and y tile, return lon, lat

   
def get_polyfill(poly):
  # given an polygon of interger numbers, generate every point so as to fill the polygon.
```
### GenerateFarmObjects
This generates an intermediate object file that could be used more effectivly as the json provided could not be streamed object by object effectivly. 
To use there is currently no run parameters option so it have to manually change the variables.

```py
def worker(data):
  # extract each object from json
  # for each object generate an farmobject and add to a result list
  # at the end dump the entire list of farm objects into a 'filename.dump' using pickle

class FarmObject:
    """
    Serializeable data, contation all region polygons that encapsulate a single farm.
    """
    def __init__(self, raw_data):
      # from the geojson, generate data.
      # note that the poly objects can "clip" into other regions (regions being tiles as described in poly), hence there is a need to add edge points,
      # 2 methods was deviced, currently a naive implementation is in place, however there is a major issue regarding this. 
      # issue 1 the data is weirdly rotated so the actual x, y seems to be of... i was looking if it wasn't appropriate to rotate all pixel values in here. but it is yet to be 
      # tested. The weird rotation is an issue where the image pixels we get seems to be rotated 90 degrees clockwise, to fix do a 90degre counter clockwise move. for now 
      # LinearSweep does do the rotation on all points before generating the finall label
      # the generated edge points can be disabled by commenting out this section (line 60 in the actual file)
      
            if len(self.regions) > 1:
                self.intersect_region()

    def intersect_region(self):
        #


    def bound_intersection(self, box1, box2, dx, dy,bounds):
        """ Finds regions bounds intersection, assuming it is convex

        Args:
            box1 ([[int]]):  polygon that clip into region 1 based on its pixel values for that specific region
            box2 ([[int]]): polygon that clip into region 2 based on its pixel values for that specific region
            dx (int): the relative x between region1 and 2 based on is tile number
            dy (int): the relative y between region1 and 2 based on is tile number
            bounds ((int, int)): the bounding box of the region based on its pixel value

        Returns:
            [[r1][r2]]: intersection points to region 1 (r1), and region 2 (r2)
        """


def main():
    # step 1 load json
    # step 2 divide into regions
     n = int(len(data)/100)
    regions = [data[i:i + n] for i in range(0, len(data), n)]
    # where 100 is the number of regions we want to divide the data into, and we will get at least 100 regions. 
    # each region will contain a part of the data like so: [[fragment], [fragment] ... [fragment]]
    # step 3. execute in a process pool, maping the regions we generated to the worker, each worker will work parallel with its fragment.
    
def load_Obj(fn):
  # function that loads a farmobject for use outside this file. 
  # this is usually what you want to call when loading one of the files.
  # dont forget to import farmobject aswell
 
```
To run the main in generateFarmObjects it requires in the same workfolder, a folder called 'obj'. it will take the id of the last item it added and name the file "{id}.dump" into obj folder. It will contain what farmobject contained. There is currently some translation error going on here.
Parameters that can change. max workers and number of regions. Dividing into more region reduces memory usage but generates more files, while more workers reduces the time to execute but massivly increases the cpu load.

### FetchImages
This is a class that fetches all images of tiles found in './data/train' folder, from mapbox api.
requires that a file called api exist in the same folder as this file. 

When run it will fetch n images at a time and will store the image in './data/train/{x}{y}.png' 
the input data to multi fetch must be a tile name, that is 'x.y'
```py
def run_multi_fetch(data, n, file_path):

run_multi_fetch([string of tile names], size of each segment, path where to dump the files)   
```
this method currenty does not seem to work when called from an other class, but i did not try to fix it what so ever.

### LinearSweep
This file has the intention of taking the dump object generated by generatefarmobjects file, and then do the following procedure:
* Load segments
* Generate np files for the first fragment
* Sweep every farm object in all dump objects in ./obj

This is a multiprocess streaming algorithm that takes a set number of segments, loads them in memory then spawns a process pool and executes its work order, when completed
load next segement.
```py

flist = os.listdir('./obj')


def load_segment(seg) -> [FarmObject]: 
    # loads a list of objects, say nr 5 to nr 10 and returns an array of farmobjects
    
def farm_object_procedure(farms): 
    farms = [farm for obj in farms for farm in obj] # flatten
    # generate n sized framgents
    n = int(len(farms)/120)
    # map to a process pool executor to worker
    
def work(region):
    # generate a np file if it does not exist
    # rotate farmobject 90 degrees clockwise
    # add new label to old, ( or a empty (256,256) array if the object did not exist)
    # dump the new label in a np file in './data/train' folder will generate new objects if encounterd
    
def sweeper(region):
    # will check if the file exist or not for a farm objects regions. 
    # if it does, rotate the label from the loaded segment, add to the old and save back to its np file

def sweep_procedure(farms):
    # same as other procedure, however this does not generate new files, only complements existing ones
    # comment out the forloop and de comment the process pool executor
    

def process_segment(start, end):
    # intermediate step to sweep, a relic of old code
    # just makes sure that everything stated maps to its corresponding segments

def generate_data(start, end):
    # intermediate step to sweep, a relic of old code
     


def main():
    segments = list(range(0, len(flist), 10)) # modify this to change the number of segments selected
    segments = [[segments[i-1], d]
                for i, d in enumerate(segments) if i != 0]  # split into ranges such that it in the end looks like this: [[0,10], [10,20] ...] 

    for every segment do a procedure on that fragment
```

Currently there is some bug where many files gets skipped. could be many files simply have a single polygon, in which case it ignores it, altho that is the intetion but it could be the cause of issues.
## allocate_data
helper function, just moves by a probability files to there respective folder for train, validation and testing. 
