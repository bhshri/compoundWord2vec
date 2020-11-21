wget https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2

wget http://medialab.di.unipi.it/Project/SemaWiki/Tools/WikiExtractor.py

python -m wikiextractor.WikiExtractor -c -b 500M --processes 4 -o . dewiki-latest-pages-articles.xml.bz2

for i in 00 01 02 03 04 05 06 07 08 09 10 11; do
 find . -name wiki_$i.bz2 \! -exec bzip2 -k -c -d {} \; > tempwiki.xml
 cat tempwiki.xml | tr '\n' ' ' > prec_tempwiki.xml
 sed -i 's/<\/doc>/\n/g' prec_tempwiki.xml
 sed -i 's/<[^>]*>//g' prec_tempwiki.xml
 sed -i 's/[0-9]//g' prec_tempwiki.xml
 cat prec_tempwiki.xml | tr '[:upper:]' '[:lower:]' > prec_lower_tempwiki.xml
 sed -i 's/[^[:alnum:] -]//g' prec_lower_tempwiki.xml
 cat prec_lower_tempwiki.xml >> final_prec_wiki.txt 
 rm -rf *.xml
 echo $i 
done


for i in 2007 2008 2009 2010 2011 2012 2013; do
 wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.$i.de.shuffled.gz
 gzip -d news.$i.de.shuffled.gz
 sed -i -e 's!http[s]\?://\S*!!g' news.$i.de.shuffled
 sed -i 's/[0-9]//g' news.$i.de.shuffled
 cat news.$i.de.shuffled | tr '[:upper:]' '[:lower:]' > prec_news.$i.de.shuffled
 sed -i 's/[^[:alnum:] -]//g' prec_news.$i.de.shuffled
 cat prec_news.$i.de.shuffled >> final_german_smt_text.txt
 rm -rf *$i.de.shuffled
done

cat final_german_smt_text.txt >> final_prec_wiki.txt
mv final_prec_wiki.txt text_corpus.txt
