pyquery: a jquery-like library for python
=========================================

.. image:: https://github.com/gawel/pyquery/actions/workflows/tox.yml/badge.svg
   :alt: Build Status
   :target: https://github.com/gawel/pyquery/actions/workflows/tox.yml

pyquery allows you to make jquery queries on xml documents.
The API is as much as possible similar to jquery. pyquery uses lxml for fast
xml and html manipulation.

This is not (or at least not yet) a library to produce or interact with
javascript code. I just liked the jquery API and I missed it in python so I
told myself "Hey let's make jquery in python". This is the result.

The `project`_ is being actively developed on a git repository on Github. I
have the policy of giving push access to anyone who wants it and then reviewing
what they do. So if you want to contribute just email me.

Please report bugs on the `github
<https://github.com/gawel/pyquery/issues>`_ issue
tracker.

.. _deliverance: http://www.gawel.org/weblog/en/2008/12/skinning-with-pyquery-and-deliverance
.. _project: https://github.com/gawel/pyquery/

..
   >>> (urlopen, your_url, path_to_html_file) = getfixture('readme_fixt')

Quickstart
==========

You can use the PyQuery class to load an xml document from a string, a lxml
document, from a file or from an url::

    >>> from pyquery import PyQuery as pq
    >>> from lxml import etree
    >>> import urllib
    >>> d = pq("<html></html>")
    >>> d = pq(etree.fromstring("<html></html>"))
    >>> d = pq(url=your_url)
    >>> d = pq(url=your_url,
    ...        opener=lambda url, **kw: urlopen(url).read())
    >>> d = pq(filename=path_to_html_file)

Now d is like the $ in jquery::

    >>> d("#hello")
    [<p#hello.hello>]
    >>> p = d("#hello")
    >>> print(p.html())
    Hello world !
    >>> p.html("you know <a href='http://python.org/'>Python</a> rocks")
    [<p#hello.hello>]
    >>> print(p.html())
    you know <a href="http://python.org/">Python</a> rocks
    >>> print(p.text())
    you know Python rocks

You can use some of the pseudo classes that are available in jQuery but that
are not standard in css such as :first :last :even :odd :eq :lt :gt :checked
:selected :file::

    >>> d('p:first')
    [<p#hello.hello>]



## 🌐 Web Resources & Interactive Index
- [TOWER CRUSH](https://iskillquest.pages.dev/tower-crush.html)
- [GRAVITY MATCHER](https://iskillplay.web.app/gravity-matcher.html)
- [CATEGORY GROW99](https://themindplays.pages.dev/category-grow99.html)
- [MAGNET TRUCK](https://studyplayings.pages.dev/magnet-truck.html)
- [CATEGORY AGILITY 3](https://themindplay.pages.dev/category-agility-3.html)
- [CUBE TO HOLE PUZZLE](https://studyplayings.web.app/cube-to-hole-puzzle.html)
- [FLYORDIEIO](https://iskillquest.pages.dev/flyordieio.html)
- [WONDERS OF EGYPT MATCH 2](https://quizverses.github.io/wonders-of-egypt-match-2.html)
- [CATEGORY TOWER DEFENSE](https://quizverses.pages.dev/category-tower-defense.html)
- [FACE CHANGES](https://iskillquest.pages.dev/face-changes.html)
- [CATEGORY SECURLY BYPASS](https://quizverses-9d2f2.web.app/category-securly-bypass.html)
- [SLAP AND RUN](https://iskillquest.pages.dev/slap-and-run.html)
- [HIDDEN OBJECTS ISLAND SECRETS](https://quizverses.github.io/hidden-objects-island-secrets.html)
- [CATEGORY CASUAL 5](https://skillplay.github.io/category-casual-5.html)
- [PHYSICS BOX 2](https://themindplay.github.io/physics-box-2.html)
- [CATEGORY SOLITAIRE](https://studyplaying.github.io/category-solitaire.html)
- [SHOT CAN WILD](https://themindplay.pages.dev/shot-can-wild.html)
- [CATEGORY LOGIC538](https://quizverses.github.io/category-logic538.html)
- [CATEGORY QUIZ40](https://studyplaying.github.io/category-quiz40.html)
- [CATEGORY STICKMAN](https://iskillquest.pages.dev/category-stickman.html)
- [SHOOT N CRUSH](https://themindplay.github.io/shoot-n-crush.html)
- [HUNGRY CORGI CUTE MUSIC GAME](https://learnquester.github.io/hungry-corgi-cute-music-game.html)
- [CUBE DROP PUZZLE](https://quizverses-9d2f2.web.app/cube-drop-puzzle.html)
- [INDEX14](https://studyplayings.web.app/index14.html)
- [CATEGORY MATCH 3117](https://studyplayings.pages.dev/category-match-3117.html)
- [INDEX14](https://quizverses.github.io/index14.html)
- [FOREST GLADE MYSTERIES](https://iskillquest.pages.dev/forest-glade-mysteries.html)
- [CATEGORY SOCCER](https://studyplayings.pages.dev/category-soccer.html)
- [ZEN MASTER 3 TILES](https://themindplay.pages.dev/zen-master-3-tiles.html)
- [CATEGORY RELAXING223](https://studyplayings.pages.dev/category-relaxing223.html)
- [CATEGORY UNBLOCKED GAMES](https://studyplayings.pages.dev/category-unblocked-games.html)
- [BUBBLE SHOOTER ULTIMATE](https://themindplay.pages.dev/bubble-shooter-ultimate.html)
- [CATEGORY BUILDING179](https://studyquests.github.io/category-building179.html)
- [LAST TO LEAVE CIRCLE OBBY](https://themindplay.github.io/last-to-leave-circle-obby.html)
- [BATTLEDUDES IO](https://studyplayings.web.app/battledudes-io.html)
- [CATEGORY RACING DRIVING](https://studyplayings.pages.dev/category-racing-driving.html)
- [FISH KINGDOM](https://iskillquest.pages.dev/fish-kingdom.html)
- [TATTOO MASTER](https://studyplayings.web.app/tattoo-master.html)
- [WRECK THE TOWER](https://themindplaying.web.app/wreck-the-tower.html)
- [UNCLE HIT PUNCH THE DUMMY](https://quizverses.github.io/uncle-hit-punch-the-dummy.html)
- [HEADLEG DASH PARKOUR](https://themindplay.pages.dev/headleg-dash-parkour.html)
- [DELICIOUS EMILYS NEW BEGINNING VALENTINES EDITION](https://quizverses-9d2f2.web.app/delicious-emilys-new-beginning-valentines-edition.html)
- [SWORDSMAN ADVENTURE](https://studyquests.pages.dev/swordsman-adventure.html)
- [CATEGORY CAT55](https://studyplayings.web.app/category-cat55.html)
- [CRAZY BUS STATION](https://themindplay.github.io/crazy-bus-station.html)
- [CUPIDS STORY LOVE ARCHER BOW](https://iskillquest.pages.dev/cupids-story-love-archer-bow.html)
- [FOREST MATCH 4](https://quizverses-9d2f2.web.app/forest-match-4.html)
- [CATEGORY ANIMAL](https://studyplayings.web.app/category-animal.html)
- [SNAKE GO ESCAPE PUZZLE](https://quizverses-9d2f2.web.app/snake-go-escape-puzzle.html)
- [TILE MATCH THE IMMERSIVE PUZZLE](https://themindzone.pages.dev/tile-match-the-immersive-puzzle.html)
- [US ARMY CAR GAMES TRUCK DRIVING](https://thelearnquesters.pages.dev/us-army-car-games-truck-driving.html)
- [POP PARTY SUIKA WATERMELON](https://studyplayings.web.app/pop-party-suika-watermelon.html)
- [FALLING ART RAGDOLL SIMULATOR](https://themindplay.pages.dev/falling-art-ragdoll-simulator.html)
- [CATEGORY MOBILE2 112 2](https://studyplaying.github.io/category-mobile2-112-2.html)
- [MERGE FLOW](https://quizverses-9d2f2.web.app/merge-flow.html)
- [CATEGORY JIGSAW](https://studyplaying.github.io/category-jigsaw.html)
- [DYNAMONS 11](https://thequizzone.pages.dev/dynamons-11.html)
- [SERIOUS HEAD 2](https://quizverses-9d2f2.web.app/serious-head-2.html)
- [CATEGORY TANK58](https://studyplayings.pages.dev/category-tank58.html)
- [IDLE BATHROOM EMPIRE TYCOON](https://quizverses.github.io/idle-bathroom-empire-tycoon.html)
- [CATEGORY SIMULATION 3](https://studyplayings.pages.dev/category-simulation-3.html)
- [THE COUNTERFEIT BANK](https://thelearnquesters.pages.dev/the-counterfeit-bank.html)
- [ZENITH RUSH](https://studyquests.github.io/zenith-rush.html)
- [CUBE SPEED DASH](https://iskillquest.pages.dev/cube-speed-dash.html)
- [PERFECT CAKE MAKER](https://studyplayings.web.app/perfect-cake-maker.html)
- [PUZZLE WOOD BLOCK](https://themindplay.github.io/puzzle-wood-block.html)
- [SNIPER 3D ZOMBIE](https://skillplay.github.io/sniper-3d-zombie.html)
- [CATEGORY BLOCK91](https://studyplayings.web.app/category-block91.html)
- [CUBEREALM IO](https://studyquesthub.web.app/cuberealm-io.html)
- [VOLLEY BEAN](https://quizverses-9d2f2.web.app/volley-bean.html)
- [LIGHT LINE](https://thequizzone.pages.dev/light-line.html)
- [CATEGORY DESTROY](https://studyquests.pages.dev/category-destroy.html)
- [BUBBLE SHOOTER WONDERS OF EGYPT](https://themindplays.pages.dev/bubble-shooter-wonders-of-egypt.html)
- [INDEX2](https://quizverses.github.io/index2.html)
- [GEOMETRY LITE](https://themindplays.pages.dev/geometry-lite.html)
- [FRUIT MERGE ARENA](https://thequizzone.pages.dev/fruit-merge-arena.html)
- [ACCURATE 2D](https://themindplay.github.io/accurate-2d.html)
- [CATEGORY POOL](https://thequizzone.pages.dev/category-pool.html)
- [FARM VS ZOMBIES](https://thequizzone.pages.dev/farm-vs-zombies.html)
- [SANTA GO](https://themindplays.pages.dev/santa-go.html)
- [CATEGORY YOUTUBE](https://thequizzone.pages.dev/category-youtube.html)
- [DONT TAP](https://thequizzone.pages.dev/dont-tap.html)
- [CATEGORY BASKETBALL](https://studyquests.pages.dev/category-basketball.html)
- [CATEGORY RACING DRIVING 2](https://studyplayings.pages.dev/category-racing-driving-2.html)
- [TRIAL XTREME](https://themindplaying.web.app/trial-xtreme.html)
- [WORD SOLITAIRE](https://thequizzone.pages.dev/word-solitaire.html)
- [NONOGRAM MASTER](https://thelearnquesters.pages.dev/nonogram-master.html)
- [UNSCREW THEM ALL](https://quizverses.github.io/unscrew-them-all.html)
- [MERGE GALAXY](https://themindplays.pages.dev/merge-galaxy.html)
- [ESCAPE THE HORROR CRAFT](https://thequizzone.pages.dev/escape-the-horror-craft.html)
- [INDEX13](https://themindplaying.web.app/index13.html)
- [BUBBLE SHOOTER WONDERS OF EGYPT](https://studyplayings.pages.dev/bubble-shooter-wonders-of-egypt.html)
- [ROYAL JEWELS MATCH](https://themindplaying.web.app/royal-jewels-match.html)
- [NOOBHOOD HALLOWEENCRAFT](https://themindplays.pages.dev/noobhood-halloweencraft.html)
- [WINTER HEXA STACK](https://studyplayings.web.app/winter-hexa-stack.html)
- [TIMEWARRIORS](https://studyquesthub.web.app/timewarriors.html)
- [SPIDER SOLITAIRE 2 SUITS](https://studyquesthub.web.app/spider-solitaire-2-suits.html)
- [MERGE PLANETS](https://studyquesthub.web.app/merge-planets.html)
- [CATEGORY PUZZLE 3](https://themindplaying.web.app/category-puzzle-3.html)
- [WOOL SORTING](https://thequizzone.pages.dev/wool-sorting.html)
- [MAD DASH](https://studyplayings.pages.dev/mad-dash.html)
- [INDEX13](https://quizverses.github.io/index13.html)
- [CATEGORY ANIMAL](https://quizverses.github.io/category-animal.html)
- [SLIPPERY DRIFT RACING](https://quizverses-9d2f2.web.app/slippery-drift-racing.html)
- [MAHJONG ADVENTURE WORLD QUEST](https://themindplay.pages.dev/mahjong-adventure-world-quest.html)
- [CATEGORY STICKMAN 2](https://studyplayings.pages.dev/category-stickman-2.html)
- [CATEGORY CARDS](https://studyplayings.web.app/category-cards.html)
- [JUST LUDO](https://themindplays.pages.dev/just-ludo.html)
- [COLOR MIX JELLY MERGE](https://skillplay.github.io/color-mix-jelly-merge.html)
- [CATEGORY MINIGAMES29](https://studyplaying.github.io/category-minigames29.html)
- [HEXANAUT IO](https://studyplayings.pages.dev/hexanaut-io.html)
- [DOOMSDAY ZOMBIE TD](https://studyquesthub.web.app/doomsday-zombie-td.html)
- [HIDE AND SEEK HORROR ESCAPE](https://quizverses-9d2f2.web.app/hide-and-seek-horror-escape.html)
- [NAUTILUS SPACESHIP ESCAPE](https://thelearnquesters.pages.dev/nautilus-spaceship-escape.html)
- [NORTHERN LIGHTS THE SECRET OF THE FOREST](https://thequizzone.pages.dev/northern-lights-the-secret-of-the-forest.html)
- [TRADING GAMES PLAYTIME](https://studyquesthub.web.app/trading-games-playtime.html)
- [WATERPARK SORT](https://thelearnquesters.pages.dev/waterpark-sort.html)
- [BRAIN TEST IQ CHALLENGE 2](https://thequizzone.pages.dev/brain-test-iq-challenge-2.html)
- [SPIDER SOLITAIRE 2 SUITS](https://thequizzone.pages.dev/spider-solitaire-2-suits.html)
- [BILLIARDS 3D RUSSIAN PYRAMID](https://thequizzone.pages.dev/billiards-3d-russian-pyramid.html)
- [WORLD CUP SOCCER CAPS](https://thequizzone.pages.dev/world-cup-soccer-caps.html)
- [THE SORTING MART](https://quizverses.github.io/the-sorting-mart.html)
- [CATEGORY PUZZLE 2](https://studyplaying.github.io/category-puzzle-2.html)
- [TSUNAMI BRAINROTS ONLINE](https://thelearnquesters.pages.dev/tsunami-brainrots-online.html)
- [CLONEUP STACK YOURSELF](https://thequizzone.pages.dev/cloneup-stack-yourself.html)
- [CAR PARKING MASTER 3D REAL DRIVING SIMULATOR](https://thequizzone.pages.dev/car-parking-master-3d-real-driving-simulator.html)
- [MATCH DREAM GARDEN](https://themindplay.github.io/match-dream-garden.html)
- [UNBLOCK IT 3D](https://studyplaying.github.io/unblock-it-3d.html)
- [FLAMES FORTUNE](https://studyquesthub.web.app/flames-fortune.html)
- [FARM MATCH SEASONS 3](https://thelearnquesters.pages.dev/farm-match-seasons-3.html)
