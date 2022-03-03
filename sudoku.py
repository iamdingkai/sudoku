


import numpy as np



board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]


board=np.array(board)
board[np.where(board=='.')]=0
board=board.astype(np.int)



# print board in a nice way
def p():
    for i in range(9):
        print(board[i,0:3],' ',board[i,3:6],' ',board[i,6:9],' missing',set(range(1,10))-set(board[i,:]))
        if i%3==2:
            print('')


# slice board into 3X3 blocks
def slicing_block():
    return [board[0:3,0:3],board[0:3,3:6],board[0:3,6:9],
            board[3:6,0:3],board[3:6,3:6],board[3:6,6:9],
            board[6:9,0:3],board[6:9,3:6],board[6:9,6:9]]

# slice board into lines
def slicing_line():
    return [board[:,j] for j in range(0,9)]+[board[i,:] for i in range(0,9)]

# slice board into 3 rows 
def slicing_3rows():
    return [board[0:3,:],board[3:6,:],board[6:9,:]]

# slice board into 3 columns 
def slicing_3cols():
    return [board[:,0:3],board[:,3:6],board[:,6:9]]


def slicing_hline():
    return [board[i,:] for i in range(9)]

def slicing_vline():
    return [board[:,j] for j in range(9)]

# check if any 3X3 block has 8 numbers already:
def easy_8(blk):
    assert blk.shape==(3,3),'wrong shape of block'
    if np.sum(blk!=0)==8:
        blk[np.where(blk==0)]=sum(range(1,10))-np.sum(blk)
        print('easy 3*3 block of 8 numbers found')
    return blk

# check if only missing 1 number on a line
def easy_line(line):
    assert line.shape==(9,), 'wrong shape of line'
    if np.sum(line!=0)==8:
        line[np.where(line==0)]=sum(range(1,10))-np.sum(line)
        print('easy line of 8 numbers found')
    return line




# for 3 rows, if a number appears twice, see if we can fill in a third

def row3(arr):
    
    assert arr.shape==(3,9),'wrong shape'
        
    for i in range(1,10):
        
        if np.sum(arr==i)==2:            
            # number i has appeared in i1 and i2 row
            # only row left is [0,1,2]-[i1,i2]
            ([i1,i2],[j1,j2])=np.where(arr==i)
            i3=[x for x in [0,1,2] if x!=i1 and x!=i2][0]
            
            if j1>j2:
                j1,j2=j2,j1
            
            if j1 in range(0,3) and j2 in range(3,6):
                j3=range(6,9)
            elif j1 in range(0,3) and j2 in range(6,9):
                j3=range(3,6)
            else:
                j3=range(0,3)
            
            # now for row i3, the only row i could appear, 
            # check if we can determine where the column is 
            column_choices=[y for y in j3 if all(board[:,y]!=i) and arr[i3,y]==0]
            if len(column_choices)==1:
                arr[i3,column_choices[0]]=i
                print('number ',i,' filled by 3-row method')



# for 3 columns, if a number appears twice, see if we can fill in a third

def col3(arr):
    
    assert arr.shape==(9,3),'wrong shape'
        
    for i in range(1,10):
        
        if np.sum(arr==i)==2:            
            # number i has appeared in i1 and i2 column
            # only column left is [0,1,2]-[i1,i2]
            ([i1,i2],[j1,j2])=np.where(arr==i)
            j3=[y for y in [0,1,2] if y!=j1 and y!=j2][0]
            
            if i1>i2:
                i1,i2=i2,i1
            
            if i1 in range(0,3) and i2 in range(3,6):
                i3=range(6,9)
            elif i1 in range(0,3) and i2 in range(6,9):
                i3=range(3,6)
            else:
                i3=range(0,3)
            
            # now for column j3, the only column i could appear, 
            # check if we can determine where the row is 
            row_choices=[x for x in i3 if all(board[x,:]!=i) and arr[x,j3]==0]
            if len(row_choices)==1:
                arr[row_choices[0],j3]=i
                print('number ',i,' filled by 3-column method')




# check line with block
# For each line, there are a few missing values. If all but one 
# missing value is already in its 3X3 block, then fill. 
def check_hline_with_block(line,iline):
    # line is the current line to be checked
    # iline is the i index of the line
    
    if iline in range(0,3):
        lb=0
        ub=3
    elif iline in range(3,6):
        lb=3
        ub=6
    else:
        lb=6
        ub=9
    
    
    if np.sum(line[0:3]==0)==1: # missing only 1 element within a block
        j=np.where(line[0:3]==0)[0][0]
        candidates=set(range(1,10))-set(line)-set(board[:,j])-set(board[lb:ub,0:3].flatten())
        if len(candidates)==1:
            line[j]=list(candidates)[0]
            print('number ',line[j],' added to line ',iline)
            
    if np.sum(line[3:6]==0)==1:
        j=np.where(line[3:6]==0)[0][0]+3
        candidates=set(range(1,10))-set(line)-set(board[:,j])-set(board[lb:ub,3:6].flatten())
        if len(candidates)==1:
            line[j]=list(candidates)[0]
            print('number ',line[j],' added to line ',iline)

    if np.sum(line[6:9]==0)==1:
        j=np.where(line[6:9]==0)[0][0]+6
        candidates=set(range(1,10))-set(line)-set(board[:,j])-set(board[lb:ub,6:9].flatten())
        if len(candidates)==1:
            line[j]=list(candidates)[0]
            print('number ',line[j],' added to line ',iline)

    return line



# check line with block
# For each line, there are a few missing values. If all but one 
# missing value is already in its 3X3 block, then fill. 
def check_vline_with_block(line,jline):
    # line is the current line to be checked
    # jline is the j index of the line
    
    if jline in range(0,3):
        lb=0
        ub=3
    elif jline in range(3,6):
        lb=3
        ub=6
    else:
        lb=6
        ub=9
    
    
    if np.sum(line[0:3]==0)==1: # missing only 1 element within a block
        i=np.where(line[0:3]==0)[0][0]
        candidates=set(range(1,10))-set(line)-set(board[i,:])-set(board[0:3,lb:ub].flatten())
        if len(candidates)==1:
            line[i]=list(candidates)[0]
            print('number ',line[i],' added to line ',jline)
            
    if np.sum(line[3:6]==0)==1:
        i=np.where(line[3:6]==0)[0][0]+3
        candidates=set(range(1,10))-set(line)-set(board[i,:])-set(board[0:3,lb:ub].flatten())
        if len(candidates)==1:
            line[i]=list(candidates)[0]
            print('number ',line[i],' added to line ',jline)

    if np.sum(line[6:9]==0)==1:
        i=np.where(line[6:9]==0)[0][0]+6
        candidates=set(range(1,10))-set(line)-set(board[i,:])-set(board[0:3,lb:ub].flatten())
        if len(candidates)==1:
            line[i]=list(candidates)[0]
            print('number ',line[i],' added to line ',jline)

    return line










for _ in range(10):
    print(_,' round')
    # check if row3 applies
    for x in slicing_3rows():
        x=row3(x)
    
    
    # check if col3 applies
    for x in slicing_3cols():
        x=col3(x)
    
    
    
    # check if easy_8 applies
    for x in slicing_block():
        x=easy_8(x)
    
    # check if easy line applies
    for x in slicing_line():
        x=easy_line(x)
    
    
    for i,x in enumerate(slicing_hline()):
        x=check_hline_with_block(x,i)
        
    
    
    for j,y in enumerate(slicing_vline()):
        y=check_vline_with_block(y,j)
    print('')
    print('')

p()



