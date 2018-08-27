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

def GetClueTextandWordLength(crossword_page_tree):
    down_clue_nums = crossword_page_tree.xpath('//div[@class="crossword__clues--down"]/ol/li/@value')
    down_clue_text_and_length = crossword_page_tree.xpath('//div[@class="crossword__clues--down"]/ol/li/div[@class="crossword__clue__text"]/text()')
    
    down_clue_text = [ "".join(text.split("(")[:-1]).strip() for text in down_clue_text_and_length]
    down_clue_length = [ "("+text.split("(")[-1] for text in down_clue_text_and_length]

    down_clues = zip(down_clue_nums,down_clue_length,down_clue_text)
    
    across_clue_nums = crossword_page_tree.xpath('//div[@class="crossword__clues--across"]/ol/li/@value')
    across_clue_text_and_length = crossword_page_tree.xpath('//div[@class="crossword__clues--across"]/ol/li/div[@class="crossword__clue__text"]/text()')
    
    across_clue_text = [ "".join(text.split("(")[:-1]).strip() for text in across_clue_text_and_length]
    across_clue_length = [ "("+text.split("(")[-1] for text in across_clue_text_and_length]

    across_clues = zip(down_clue_nums,down_clue_length,down_clue_text)
    
    return across_clues, down_clues

def OutputClueDetails(crossword_id, grid_indexs, across_clues, down_clues):
    clues = []
    for clue in across_clues:
        clue_i = int(clue[0])
        clues.append( (grid_indexs[clue_i][0],grid_indexs[clue_i][1],clue[1],"across",clue[2]) )

    for clue in down_clues:
        clue_i = int(clue[0])
        clues.append( (grid_indexs[clue_i][0],grid_indexs[clue_i][1],clue[1],"down",clue[2]) )

    crossword_clue_dir = "crossword_clues"

    output_path = os.path.join(crossword_clue_dir,crossword_id+".txt")

    clue_output_text = ""

    for clue in clues:
        clue_output_text += str(clue)[1:-1] + "\n"

    clue_output_text = clue_output_text[:-1]

    with open(output_path,"w") as f:
        f.write(clue_output_text)
    

if __name__ == '__main__':

    crossword_id = "15071"
    crossword_page_tree = GetCrosswordPageTree(crossword_id)
    
    grid_indexs = GetCrosswordNumberGridIndexs(crossword_page_tree)

    print(grid_indexs)
    print("")

    across_clues, down_clues = GetClueTextandWordLength(crossword_page_tree)

    print(across_clues)
    print("")

    print(down_clues)
    print("")

    OutputClueDetails(crossword_id, grid_indexs, across_clues, down_clues)
