import re
import os
import argparse
parser = argparse.ArgumentParser(description="Author: Peng Zhao <pengzhao@nwafu.edu.cn>")
parser.add_argument('-vcf', type=str,help="VCF file")
parser.add_argument('-pos', type=str,help="Position of the SNPs")
parser.add_argument('-chr', type=str,help="Names of chromosomes")
parser.add_argument('-out', type=str,help="The prefix of the output file")
args = parser.parse_args()
vcf_name = args.vcf
pos_name = args.pos
chr_name = args.chr
out_name = args.out
inf = open(vcf_name,"r")
inf2 = open(pos_name,"r")
ouf = open("./scripts/temp/temp.vcf","w")
chr_id = chr_name
dict_1 = {}
for line2 in inf2:
    line2 = line2.replace("\n","")
    li2 = re.split("\t| ",line2)
    dict_1[li2[0]] = "1"
for line in inf:
    line = line.replace("\n","")
    li = re.split("\t| ",line)
    if li[0][:1] != "#":
        if li[0] == chr_id:
            if li[1] in dict_1:
                n = len(li)
                for i in range(9, n):
                    if li[i] == "0/0":
                        li[i] = str(li[3]) + "/" + str(li[3])
                    elif li[i] == "0/1":
                        li[i] = str(li[3]) + "/" + str(li[4])
                    elif li[i] == "1/1":
                        li[i] = str(li[4]) + "/" + str(li[4])
                li[2] = str(li[0]) + "&" + str(li[1])
                del li[0:2]
                del li[1:7]
                ouf.write("%s\n" % (li))
ouf.close()
inf3 = open("./scripts/temp/temp.vcf","r")
ouf3 = open("./scripts/temp/temp.replace.vcf","w")
for line3 in inf3:
    line3 = line3.replace("\n","").replace(" ","").replace("[","").replace("\'","").replace(",","\t").replace("]","")
    ouf3.write("%s\n" % (line3))
ouf3.close()
dos2unix_command = "dos2unix ./scripts/temp/temp.replace.vcf"
rank_command = "awk \'{for(i=1;i<=NF;i=i+1){a[NR,i]=$i}}END{for(j=1;j<=NF;j++){str=a[1,j];for(i=2;i<=NR;i++){str=str \" \" a[i,j]}print str}}\' ./scripts/temp/temp.replace.vcf > ./scripts/temp/temp.replace.rank.vcf"
plot_command = "Rscript ./scripts/LDplot.R"
mv_command = "cp " + str(pos_name) + " ./scripts/temp/snp.pos.txt"
mv_command1 = "cp ./scripts/temp/temp.replace.rank.vcf " + str(out_name) + ".snp.geno.txt"
mv_command2 = "cp ./scripts/temp/snp.pos.txt " + str(out_name) + ".snp.pos.txt"
mv_command3 = "mv ./scripts/temp/LDplot.pdf " + str(out_name) + ".pdf"
rm_command = "rm ./scripts/temp/*"
os.system(dos2unix_command)
os.system(rank_command)
os.system(mv_command)
os.system(plot_command)
os.system(mv_command1)
os.system(mv_command2)
os.system(mv_command3)
os.system(rm_command)
