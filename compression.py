import heapq,os
class BinaryTree:
    def __init__(self,key,value):
        self.left=None
        self.right=None
        self.key=key
        self.value=value
    def __lt__(self,other):
        return self.value<other.value
    def __eq__(self,other):
        return self.value==other.value
class Huffman:
    def __init__(self,path):
        self.path=path
        self.heap=[]
        self.codes={}
        self.reversecodes={}
    def __count_frequency(self,text):
        freq_dict={}
        for i in text:
            if(i in freq_dict):
                freq_dict[i]+=1
            else:
                freq_dict[i]=1
        return freq_dict
    def __buildHeap(self,freq_dict):
        for key,value in freq_dict.items():
             binaryTree_node=BinaryTree(key,value)
             heapq.heappush(self.heap,binaryTree_node)
    def __buildBinaryTree(self):
        while(len(self.heap)>1):
            binary_tree_node1=heapq.heappop(self.heap)
            binary_tree_node2=heapq.heappop(self.heap)
            sum_of_freq=binary_tree_node1.value+binary_tree_node2.value
            new_node=BinaryTree(None,sum_of_freq)
            new_node.left=binary_tree_node1
            new_node.right=binary_tree_node2
            heapq.heappush(self.heap,new_node)
        return
    def __buildBinaryTreeCodeHelper(self,root,currbits):
        if(root is None):
            return
        if(root.key is not None):
            self.codes[root.key]=currbits
            self.reversecodes[currbits]=root.key
            return
        self.__buildBinaryTreeCodeHelper(root.left,currbits+"0")
        self.__buildBinaryTreeCodeHelper(root.right,currbits+"1")
    def __buildBinaryTreeCode(self):
        root=heapq.heappop(self.heap)
        self.__buildBinaryTreeCodeHelper(root,"")
    def __buildEncodedText(self,text):
        encoded_text=""
        for letter in text:
            encoded_text+=self.codes[letter]
        return encoded_text
    def __buildPaddedText(self,encoded_text):
        padding_value=8-len(encoded_text)%8
        encoded_text+="0"*padding_value
        padding_info='{0:08b}'.format(padding_value)
        return padding_info+encoded_text
    def __buildByteArray(self,text):
        array=[]
        for i in range(0,len(text),8):
            byte=text[i:i+8]
            array.append(int(byte,2))
        return array
    def compression(self):
        #first create the path and extract data from the text file
        filename,file_extension=os.path.splitext(self.path)
        output_path=filename +'.bin'
        with open(self.path,'r+') as file, open(output_path,'wb')as output:
            text=file.read()
            text=text.rstrip()
            #count the frequency of the characters using count_frequency function
            frequency_dict=self.__count_frequency(text) 
            #construct min heap from the dictionary for minimum 2 frequency values in each step
            self.__buildHeap(frequency_dict)
            #construct binary tree from min heap
            self.__buildBinaryTree()
            #construct binary code from binary tree and store it in hashmap(dictionary)
            self.__buildBinaryTreeCode()
            #construct encoded text
            encoded_text=self.__buildEncodedText(text)
            #construct padded text
            padded_text=self.__buildPaddedText(encoded_text)
            #return the output in binary format
            byte_array=self.__buildByteArray(padded_text)
            final_bytes=bytes(byte_array)
            output.write(final_bytes)
            return output_path
    def RemovePadding(self,text):
        padding_info=text[:8]
        number_of_padding_bits=int(padding_info,2)
        text_after=text[8:-1*number_of_padding_bits]
        return text_after
    def DecodeText(self,text):
        currbits=""
        decoded_text=""
        for i in text:
            currbits+=i
            if(currbits in self.reversecodes):
                decoded_text+=self.reversecodes[currbits]
                currbits=""
        return decoded_text
    def decompression(self,input_path):
        filename,file_extension=os.path.splitext(input_path)
        output_path=filename+"_decompressed"+".txt"
        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bit_string=""
            byte=file.read(1)
            while(byte):
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read(1)
            text_after_removing_padding=self.RemovePadding(bit_string)
            decoded_text=self.DecodeText(text_after_removing_padding)
            output.write(decoded_text)
        return output_path
obj1=Huffman('final concentrations of liquids.txt')
compressed_file=obj1.compression()
obj1.decompression(compressed_file)