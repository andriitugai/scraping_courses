import re

import requests
import scrapy

from pathlib import Path

from ..items import CoursesLectionInfoItem

video_dir = 'statistics_video'

urls = [
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/describing-data-and-inferring-meaning/1148423545001_3699340258001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect01-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883aa47d00d48e15300c09dc2a8136df9ec7326e4&hdnts=st=1579178125~exp=1579264525~acl=/*~hmac=868c19973888f26a18771f002cd120970dd78229451c05d77daa727b437d5fcc',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/data-and-distributionsgetting-the-picture/1148423545001_3699339296001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect02-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae4417145066de3e3652de9fe56d10f570c7ea&hdnts=st=1579181811~exp=1579268211~acl=/*~hmac=bfa3f5eea8f628772a975b27d6ff8e442452b52f3b0b4de09528a10318478c5b',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/inferencehow-close-how-confident/1148423545001_3699326672001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect03-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae454e779fd6740816703b29fb23cc0631ff85&hdnts=st=1579181922~exp=1579268322~acl=/*~hmac=90297c30ec4b209274474817a283a8af323242e3d6c31c5eec5495c367d22351',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/describing-dispersion-or-measuring-spread/1148423545001_3699327446001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect04-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae463944ee5e0e05281bc815032b105204122b&hdnts=st=1579182007~exp=1579268407~acl=/*~hmac=72c708933817df565166c063045b504bae0ec180a87059a53452430aa33e9365',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/models-of-distributionsshapely-families/1148423545001_3699327502001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect05-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae463f46ee5e0e05281b77d8defb5cd84f3373&hdnts=st=1579182065~exp=1579268465~acl=/*~hmac=70bd17fa687a167b3790432c8f6b90e5e73e2013d01a8498f2e8dff4e0424f08',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/the-bell-curve/1148423545001_3699329199001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect06-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae4713f098ef4652aafa2195ac3980de7540ab&hdnts=st=1579182129~exp=1579268529~acl=/*~hmac=4d6fb2f122ba4498d868d77a905c13b1fc3b461eab49dee3fe9e4a1fb9c319ef',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/correlation-and-regressionmoving-together/1148423545001_3699332583001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect07-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae48ee52ac60b7887200f469362352129d348b&hdnts=st=1579182204~exp=1579268604~acl=/*~hmac=d8515a018acd2a954cbb4150e2bae4130329ba2d81cd6f14ba499d91eabe6ae3',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/probabilityworkhorse-for-inference/1148423545001_3699332653001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect08-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae48e85eac60b788720019905d2091eeb7afa8&hdnts=st=1579182268~exp=1579268668~acl=/*~hmac=fb47b5b467e68e2edcb5d5d46daf10bb84996c03720d31fcb061642e03fa43d3',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/samplesthe-few-the-chosen/1148423545001_3699334492001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect09-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae4941b76e75313498c7dedbbcf98925abd760&hdnts=st=1579182316~exp=1579268716~acl=/*~hmac=b334c7a38e8f82c1d7505bd593e3de8978c37810524cbd9d1c54bb3671224648',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/hypothesis-testinginnocent-until/1148423545001_3699332042001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect10-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ae4946b36e75313498c7248c63d7b2c78c384e&hdnts=st=1579182362~exp=1579268762~acl=/*~hmac=a3aa0f9715407811bdab1a475064a3c25b11ed7fbadbac61df305cfa8d81001a',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/confidence-intervalshow-close-how-sure/1148423545001_3699334574001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect11-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad404f6571868d08d890f83a2041ac0aa4cb1e&hdnts=st=1579182431~exp=1579268831~acl=/*~hmac=48a4dfd53adb0d29c45a6d5aa10786822cc65d91743b9de9c006e9192b19967a',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/design-of-experimentsthinking-ahead/1148423545001_3699335866001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect12-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad404b6d71868d08d890e3abde80ad77a5a466&hdnts=st=1579182479~exp=1579268879~acl=/*~hmac=3580a7cf929187b14216ca64adc815719d603acaeda6e36c59c0ab372181a03f',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/lawyoure-the-jury/1148423545001_3699339268001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect13-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad41e362e0a061bc3f061bfdb406059eab5ef7&hdnts=st=1579182558~exp=1579268958~acl=/*~hmac=b2b5cf175cd2eabe5dd67d69dd3b8894b17f05ccf03123cb27d885d9732c3a9f',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/democracy-and-arrows-impossibility-theorem/1148423545001_3699344460001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect14-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad42747bd5080f56fc286b52a58286d04dc0b1&hdnts=st=1579182614~exp=1579269014~acl=/*~hmac=84daff5b28e2b543e090899c05858c459ccd3e9ade867491a68745f6fd01b701',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/election-problems-and-engine-failure/1148423545001_3699340277001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect15-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad427276d5080f56fc287d13212ae652d0d75c&hdnts=st=1579182679~exp=1579269079~acl=/*~hmac=7571e673afd540dd1fc225a24a327f956a4533d407eb170df503d3b5fe541849',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/sportswhos-best-of-all-time/1148423545001_3699341901001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect16-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad438eb784171080d934961ec6328f9cacfa20&hdnts=st=1579182732~exp=1579269132~acl=/*~hmac=e27f0dbb24cbd646f17caf69d9e48693a5dec95d3fc6c7ad8c5b97c104659e09',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/riskwar-and-insurance/1148423545001_3699341910001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect17-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad4384b484171080d9340d80a6e8f2feb12c0a&hdnts=st=1579182791~exp=1579269191~acl=/*~hmac=5ec19613615d3fec17b33c06ce714c3df1b8ea9dbd7b69017d49bb78d1fd70c2',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/real-estateaccounting-for-value/1148423545001_3699381089001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect18-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad44d091e631d1d75a17a0bcf67527df35d3d1&hdnts=st=1579182854~exp=1579269254~acl=/*~hmac=58a26643daf7cef75fa7cbeb7dd2161202261a01d4c7c51ab317fef4f2e43170',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/misleading-distorting-and-lying/1148423545001_3699344407001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect19-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad44dc90e631d1d75a175af45eddf96410ae8b&hdnts=st=1579182895~exp=1579269295~acl=/*~hmac=9d1e21af175ead51b76c4155c2d3d6eeb1db91b2142131e6277bb182947ebb7a',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/social-scienceparsing-personalities/1148423545001_3699348881001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect20-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad45a8bd3233e1c34e812d222326d0c39bb1d0&hdnts=st=1579182939~exp=1579269339~acl=/*~hmac=5c6a9eddb40c2e80472b537ce9868be1ebf09b6e3ddbb3171cd83a53b8081fee',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/quack-medicine-good-hospitals-and-dieting/1148423545001_3699348886001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect21-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad46a5b56506c1f9c8c9382dcd51c99cb0f824&hdnts=st=1579183015~exp=1579269415~acl=/*~hmac=61902636a5592f0815a11ae15fbf085af07a2abf9d70a514a8c3aa3d754698c4',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/economicsone-way-to-find-fraud/1148423545001_3699348828001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect22-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad46a3b66506c1f9c8c93696226e693e1193aa&hdnts=st=1579183076~exp=1579269476~acl=/*~hmac=581849d5c3631582c8259f77eb3854863b762ca8efe9b5aaf9d9cb25e37a4e8b',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/sciencemendels-too-good-peas/1148423545001_3699353364001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect23-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad478a7d4db5aff824a95aebc2d586a3f956f4&hdnts=st=1579183127~exp=1579269527~acl=/*~hmac=a0fa6d34e19596c0b3e0fbbd034c9e7fbb460c951c0d1dd6d55df943929c1a3b',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/statistics-made-clear/statistics-everywhere/1148423545001_3699350458001_18170-anon-eastbaymedia-drm-courses-1487-m4v-TGC-1487-Lect24-MeaningfromDataStatistics.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad4781794db5aff824a979de021524a6ffc2a9&hdnts=st=1579183193~exp=1579269593~acl=/*~hmac=517721bd199a967ae4821de72c2c235a0642be0dad0581ea7e19d55c3b87bab4'
]

urls_italy = [
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_01/3032_01_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ad4896c2caa8331ad6ad7bc8f4b5cff5ffd1cb&hdnts=st=1579183285~exp=1579269685~acl=/*~hmac=a975c33b2fe7d453bc457246cb895577838e7ac58fa8e8c3c22e5cc8143a2607',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_02/3032_02_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac417e34f2f7813e45d923e799fadbaf3d5c1b&hdnts=st=1579183504~exp=1579269904~acl=/*~hmac=f167010a7cefddd2945afb67e6d03dcc23ba283166ba71df5542163f7da7cd7b',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_03_/3032_03_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac417a33f2f7813e45d913358dc38d7777c496&hdnts=st=1579183543~exp=1579269943~acl=/*~hmac=8b25fee0c724ce752c98bfb8ca1bbb8aeba8ccbcaac48e70a67eaad62bb4c274',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_04/3032_04_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac417633f2f7813e45d9132d976c18f2c1fd2a&hdnts=st=1579183583~exp=1579269983~acl=/*~hmac=f14c09b227f823f1645c06c6e0b234a794e49bef28c098db496c6b84234d19d3',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_05/3032_05_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac42b9ee70622a2f7a2e6a33a0934a41b2bff3&hdnts=st=1579183641~exp=1579270041~acl=/*~hmac=8d6ba408d7ab04a2d7c2d9761c3af1b41be9b94ddaee724eb77f536d01019b04',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_06/3032_06_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac42b5ea70622a2f7a2e093a99b94864331427&hdnts=st=1579183685~exp=1579270085~acl=/*~hmac=491e099338ec17949f3ed8f58137a661a7a910e3544f331347c87d7176d46bbf',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_07/3032_07_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac439dabe6e93f4baaa1a0f40158da0e8546dc&hdnts=st=1579183723~exp=1579270123~acl=/*~hmac=b519036ae075c2ff5208f37a0ecd4753263e3244d99ca8ba56685b07375101ab',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032__08/3032-08_FIX_mpeg_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac4398aee6e93f4baaa1a9191dc3600fa6e582&hdnts=st=1579183776~exp=1579270176~acl=/*~hmac=d4bfcb16405cc0103e345d9ac756011c5298d76e1950d9e82e331e61973c0e03',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_09/3032_09_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac44a94fe2dddca3014b58cc11e7e5960741a5&hdnts=st=1579183821~exp=1579270221~acl=/*~hmac=4ebaa03e2a8955b56b3da3ea7546cccd83f7ab6c077b3782e933bc8916b9ec7e',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_10/3032_10_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883ac44ad46e2dddca3014bdeaa5c806027d85f86&hdnts=st=1579183868~exp=1579270268~acl=/*~hmac=a290c4d77a37bd2d0a9a42f19df71c23e3547ebe1f9e4bc46085f70a8df1eaca',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_11/3032_11_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3467163b8e8fd990bc93cc25a23668895e5ee&hdnts=st=1579185085~exp=1579271485~acl=/*~hmac=72fece31518d656453da884cf14af10b36d515221216d5c97853651cdf082efe',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_12/3032_12_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a34766945cfa8e5f0c86e7c8bf4e04b5403fce&hdnts=st=1579185126~exp=1579271526~acl=/*~hmac=56e0605dc18217147e099b91a225148babff0d4909b4f2c9db0d773ab23a4559',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_13/3032_13_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3476c935cfa8e5f0c86d8cba42bbdbfd3d8ca&hdnts=st=1579185181~exp=1579271581~acl=/*~hmac=ffc25fa2b9298e7ed210fc0549dc3179def7df20ff6603c5dc2d8218c7b82216',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_14/3032_14_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3484f52813716c4f555568c3c809fe44e5edd&hdnts=st=1579185235~exp=1579271635~acl=/*~hmac=a024c1939a725ef8e239190a7e4ddfb361312baa9d1fcef3aaa7d7af54f7dd95',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_15/3032_15_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3484452813716c4f555f2388b43ae102ed89b&hdnts=st=1579185285~exp=1579271685~acl=/*~hmac=e98350e6005c17f926ca7ce7184c9ebf878267fd3665c202c744039b93d8402d',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_16/3032_16_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3492104826424552ff7fd7cba42e32891059a&hdnts=st=1579185321~exp=1579271721~acl=/*~hmac=626fa7c4c249edc84761d898abb4339bde1d60e086658a30e9fdaaf4a522e3d0',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_17/3032_17_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3492600826424552ff734c1ce0f24f43dabaf&hdnts=st=1579185355~exp=1579271755~acl=/*~hmac=eb6a78a3a0824af27e5ba68a49d2838184843bc68d2184abe8ab8f6738f32885',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_18/3032_18_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a3492a05826424552ff753f5290a95fa8e86ed&hdnts=st=1579185390~exp=1579271790~acl=/*~hmac=efca34fe7e4cf2ace0ae23c8320f1dd2cb15524b825f4fe9345e7f4cbb9f5219',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_19/3032_19_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2405522953552809087d6abb67fedd725c6fc&hdnts=st=1579185439~exp=1579271839~acl=/*~hmac=dc6789a9ecbe83be6f632b4a2652115526223616d8315d0fb54789c102deaa9a',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032__20/3032-20_FIX2_EXPORT_mpeg_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a240512c953552809087c7990766e940a77f0e&hdnts=st=1579185477~exp=1579271877~acl=/*~hmac=acc9b1d08bcc971e153c94ba9253735f6eaf04dabad4cfbe42f4ccbc4cb78478',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_21/3032_21_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a241847daf79674fa55fe6beb31a28e1a030f6&hdnts=st=1579185546~exp=1579271946~acl=/*~hmac=7493655d478f49c1972c398f9ef337be858dfd9b85f268ff8d9635c59ba201b5',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_22/3032_22_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a241887caf79674fa55f857b8400dbd4e8edac&hdnts=st=1579185587~exp=1579271987~acl=/*~hmac=7fd17e35de0684a6e84fc27f88b8042dc599ac9869c2700d87df7d9bad6bf4b7',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_23/3032_23_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a242741a92ad99816e38266539aabb52ba9e3f&hdnts=st=1579185631~exp=1579272031~acl=/*~hmac=18c9e7428e27b5b7609c069e7315a361be56c476d53f48a8120436d8556aa425',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_24/3032_24_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a242711292ad99816e38466f6f69f80fa8c959&hdnts=st=1579185669~exp=1579272069~acl=/*~hmac=e729aa879b8f4958ca7c27298d232bf8b5f2834e4e950d2978ae6042dbf6a0ab',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_25/3032_25_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2434dc27c1a693a6bf22f63f26bed2ab1908e&hdnts=st=1579185714~exp=1579272114~acl=/*~hmac=98370e42f6f1b46619c8906cd8aa590d8ffae80a25f93c56ccb738ec21a2c6ec',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_26/3032_26_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a24349c67c1a693a6bf2e39acfb1a7e41f8797&hdnts=st=1579185750~exp=1579272150~acl=/*~hmac=56d743d8d833094a5d5274cbd6ca3cc85b4bcf73f58340f5955cb7845a733c05',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_27/3032_27_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a24344c37c1a693a6bf289ce364d73defe3d6f&hdnts=st=1579185785~exp=1579272185~acl=/*~hmac=f42008ce6855e62643ed7bf0bfa93f1a4dd82c5118abc16ef003fda610b2a178',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_28/3032_28_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a244d0d09299c7ee901eb52ef8538173f54389&hdnts=st=1579185823~exp=1579272223~acl=/*~hmac=981ecd4b28de6009ac53ace4b9a2e4db4cbec3026050d0816171b9b1fc835c2c',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032__29/3032-29_FIX_mpeg_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a244dbd79299c7ee901e630f46c00767205275&hdnts=st=1579185894~exp=1579272294~acl=/*~hmac=9a0d177b38d47c8537b62ea854493bb0d02224307ce73607912316381e272d54',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_30/3032_30_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2456ad83306927c782ae91fbf8a7e147fdf5c&hdnts=st=1579185960~exp=1579272360~acl=/*~hmac=58baecdd36b94ba64a788c08d084fb6fbfd8792241993c437a8b998caaf20122',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_31/3032_31_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a24565df3306927c782a62bde4844babb48799&hdnts=st=1579185997~exp=1579272397~acl=/*~hmac=581d52901ebeb3f5549875618156307af0419f3884f4621a309b90ae6ab2be8e',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_32/3032_32_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2465199393a24c81880a577e899caac294f8c&hdnts=st=1579186039~exp=1579272439~acl=/*~hmac=e898c9f687b52a718edcf80796f29e9b6fe97a3264904bb981d27a9ce1eb83fd',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_33/3032_33_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2465a91393a24c818804d98f3ad36e4c4c2be&hdnts=st=1579186081~exp=1579272481~acl=/*~hmac=0e229c1a072a36dd5c58fb519b4b527623f37526b5f63d2b403f83d4d4804a30',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_34/3032_34_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2477907a4d84995de827a2bd17d1bab6e7b51&hdnts=st=1579186133~exp=1579272533~acl=/*~hmac=98be521b2dab4aa0ec25436c0506f6565945a02e6f37ee8df5365870c9fa1c14',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_35/3032_35_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a2477306a4d84995de82c2a8a6ac04a7b98b69&hdnts=st=1579186192~exp=1579272592~acl=/*~hmac=d2245463dd6d59c30e2f96af9d18e48b74007b7674169e987e134be152de5bfa',
    'https://vtgc.viewlift.com/video_assets/2015/mp4/3032/3032_36/3032_36_6912kbps.mp4?7544bdcc50dae6fd8d8ebeb3ba54706c7eb1db7bd808eb469b2093bb2883a248c209d941132525335963acbf3ef2646eb7&hdnts=st=1579186235~exp=1579272635~acl=/*~hmac=a165c961242122d889738e63db91150661efcef76a40e35c908b24811f383be7'
]


class GcpSpider(scrapy.Spider):
    name = 'gcp_spider'
    # allowed_domains = ['clever-lichterman-044f16.netlify.com/']

    def start_requests(self):
        start_urls = [
            'https://www.thegreatcoursesplus.com/statistics-made-clear'
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = CoursesLectionInfoItem()

        all_lectures_info = response.css(
            "div.module-container.show-dynamic-trays > div > div > div"
        )

        # numbers = all_lectures_info.css(
        #     "div.list-tray-item-index-container span::text").getall()
        # titles = all_lectures_info.css(
        #     "div.list-tray-item-title::text").getall()
        urls = all_lectures_info.css("div > a::attr(href)").getall()

        for url in urls:
            yield response.follow(url=url, callback=self.parse2)

    def parse2(self, response):

        item = CoursesLectionInfoItem()

        item['number'] = response.css(
            'div.layout-module.lecture-top > div::text').get()
        item['lect_title'] = response.css(
            'div.layout-module.lecture-top > h1::text').get()

        if item['number'] in ['3', '7', '11']:
            l_num = int(item['number'])
            url = urls[l_num-1]

            file_name = f'{l_num:02}-' + \
                re.sub(r'[\W_]+', '-', item['lect_title']) + '.mp4'

            path = Path.cwd()/video_dir/file_name

            myfile = requests.get(url)
            with open(path, 'wb') as download:
                download.write(myfile.content)
                print(f'{path} has been loaded!')

        yield item
