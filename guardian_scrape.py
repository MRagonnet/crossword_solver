from lxml import html
import requests
import os

def GetCrosswordPageTree(crossword_id):
    base_url = "https://www.theguardian.com/crosswords/quick/{crossword_id}"
    crossword_save_dir = "crossword_pages"

    if(os.path.exists(os.path.join(crossword_save_dir, crossword_id+".txt"))):
        tree = html.fromstring(LoadCrosswordPageText(crossword_id))
    else:    
        crossword_url = base_url.format(crossword_id=crossword_id)

        page = requests.get(crossword_url)

        SaveCrosswordPageText(page,crossword_id)

        tree = html.fromstring(page.content)

    return tree


def SaveCrosswordPageText(page,crossword_id):
    crossword_save_dir = "crossword_pages"
    with open(os.path.join(crossword_save_dir, crossword_id+".txt"),"w") as f:
        f.write(page.content)


def LoadCrosswordPageText(crossword_id):
    crossword_save_dir = "crossword_pages"

    crossword_text = ""
    with open(os.path.join(crossword_save_dir, crossword_id+".txt"),"r") as f:
        crossword_text = f.read()

    return crossword_text

def GetCrosswordNumberGridIndexs(crossword_page_tree):
    number_x_values = crossword_page_tree.xpath('//text[@class="crossword__cell-number"]/@x')
    number_y_values = crossword_page_tree.xpath('//text[@class="crossword__cell-number"]/@y')
    
    number_coords = zip([float(x) for x in number_x_values],[float(y) for y in number_y_values])

    # print(number_coords)

    #2 #386
    x_start = 2
    
    #step 32
    coord_step = 32
    
    #10 #394
    y_start = 10

    grid_indexs = []
    for x_coord,y_coord in number_coords:
        grid_indexs.append( (int((y_coord - y_start)/coord_step),int((x_coord - x_start)/coord_step)) )

    return grid_indexs


if __name__ == '__main__':

    crossword_id = "15071"
    crossword_page_tree = GetCrosswordPageTree(crossword_id)
    
    grid_indexs = GetCrosswordNumberGridIndexs(crossword_page_tree)

    print(grid_indexs)


