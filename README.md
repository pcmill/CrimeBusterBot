# CrimeBusterBot
Project for the Dutch Open Hackathon 2018 #doh18

THIS IS NOT A FINISHED PRODUCT. These are sniplets of code to proof and demonstrate our model for the Hackathon. A lot of the code is designed to use the NL zone file, which is not public data. So you will not be able to run this.

### High Risk Site dumps 
You will see some text files with high risk/fake sites. These were auto detected by our software. It can absolutly have 'false positives', meaning it can include legitimate sites. We will try to improve our engine over time, to lower the risk of 'false positives'.

### Introduction

This tool takes a website name and analysis some parameters to detect if the
website is bogus.

We are analysing the content of the website, TLS/SSL certificate, *whois*
information, police and kadaster data, machine learning tools and other
attributes.

As an additional feature, the product also detects other similar websites
using content analysis and machine learning supervised algorithms.

### Possible improvments

- Domain scanners, such as *nmap*, *striker* etc.
- DNS analysers, such as *https://dnslytics.com*.
- Online analysers, such as [*urlvoid*](http://www.urlvoid.com/).
- Extend existing features.
