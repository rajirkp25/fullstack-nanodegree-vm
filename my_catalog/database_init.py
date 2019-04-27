from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import User, Category, CategoryItem
# from astroid.__pkginfo__ import description
import random

engine = create_engine('sqlite:///bookcats.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# tile background list for random selection for ui

tile_color_list = ['bg-secondary', 'bg-primary', 'bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'bg-dark']

# Create dummy user
user1 = User(name="Raji Rama", email="rajir.home@gmail.com",
             avatar='https://cdn.theatlantic.com/assets/media/img/mt/2017/10/Pict1_Ursinia_calendulifolia/lead_720_405.jpg?mod=1533691909')
session.add(user1)

user2 = User(name="Veda Ayala", email="veda.ayala@gmail.com",
             avatar='https://cdn.theatlantic.com/assets/media/img/mt/2017/10/Pict1_Ursinia_calendulifolia/lead_720_405.jpg?mod=1533691909')
session.add(user2)

user3 = User(name="Koutilya Vish", email="koutilya.vish@gmail.com",
             avatar='https://cdn.theatlantic.com/assets/media/img/mt/2017/10/Pict1_Ursinia_calendulifolia/lead_720_405.jpg?mod=1533691909')
session.add(user3)

session.commit()
# categories

cat1 = Category(name="Sci-Fi", description="Science fiction (often shortened to Sci-Fi or SF) is a genre of speculative fiction, typically dealing with imaginative and futuristic concepts such as advanced science and technology, space exploration, time travel, and extraterrestrials in fiction. Science fiction often explores the potential consequences of scientific other various innovations, and has been called a literature of ideas", tile="bg-secondary", user=user1)

session.add(cat1)

cat2 = Category(name="Children's Book Series", description="A children's book series is a set of fiction books, with a connected story line, written for children.", tile="bg-primary", user=user1)

session.add(cat2)

cat3 = Category(name="Meditation", description="Meditation is a practice where an individual uses a technique – such as mindfulness, or focusing their mind on a particular object, thought or activity – to train attention and awareness, and achieve a mentally clear and emotionally calm and stable state", tile="bg-info", user=user1)

session.add(cat3)

cat4 = Category(name="Mythology", description="In present use, mythology usually refers to the collected myths of a group of people, but may also mean the study of such myths.[31] For example, Greek mythology, Roman mythology and Hittite mythology all describe the body of myths retold among those cultures. Folklorist Alan Dundes defines myth as a sacred narrative that explains how the world and humanity evolved into their present form. Dundes classified a sacred narrative as a story that serves to define the fundamental worldview of a culture by explaining aspects of the natural world and delineating the psychological and social practices and ideals of a society. Anthropologist Bruce Lincoln defines myth as ideology in narrative form.", tile="bg-success", user=user1)

session.add(cat4)

cat5 = Category(name="Books for Wisdom", description=" These books will make you smarter. They offer wisdom that has stood the test of time, provide ideas for managing the complexities and challenges of life, and foster a greater understanding of our world.", tile="bg-warning", user=user1)

session.add(cat5)

cat6 = Category(name="Ancient History", description="Throughout the years, archaeologists have come across incredible discoveries. Some of these discoveries are ancient manuscripts which have been found to portray history from a different point of view. A controversial point of view.", tile="bg-primary", user=user1)

session.add(cat6)

cat7 = Category(name="Biography", description="A biography (from the Greek words bios meaning life, and graphos meaning write) is a non-fictional account of a person's life. Biographies are written by an author who is not the subject/focus of the book.", tile="bg-dark", user=user1)

session.add(cat7)

cat8 = Category(name="Spirituality", description="Spirituality may refer to almost any kind of meaningful activity, personal growth, or blissful experience.Traditionally, spirituality refers to a process of re-formation of the personality but there is no precise definition of spirituality.", tile=random.choice(tile_color_list), user=user1)

session.add(cat8)

cat9 = Category(name="Humor", description="A comic novel is usually a work of fiction in which the writer seeks to amuse the reader, sometimes with subtlety and as part of a carefully woven narrative, sometimes above all other considerations. It could indeed be said that comedy fiction is literary work that aims primarily to provoke laughter, but this isn't always as obvious as it first may seem.", tile="bg-warning", user=user1)

session.add(cat9)

cat10 = Category(name="Philosophy", description="Philosophy is the study of general and fundamental questions about existence, knowledge, values, reason, mind, and language. Such questions are often posed as problems to be studied or resolved. The term was probably coined by Pythagoras", tile=random.choice(tile_color_list), user=user1)

session.add(cat10)

session.commit()
# Books for Category Sci-Fi

catItem1 = CategoryItem(name="Alien invasion", description="Tolkien's seminal three-volume epic chronicles the War of the Ring, in which Frodo the hobbit and his companions set out to destroy the evil Ring of Power and restore peace to Middle-earth. The beloved trilogy still casts a long shadow, having established some of the most familiar and enduring tropes in fantasy literature. ", price="$19.50", author="H.G.Wells", category=cat1)

session.add(catItem1)

catItem2 = CategoryItem(name="The Lord Of The Rings", description="The alien invasion or space invasion is a common feature in science fiction stories and film, in which extraterrestrials invade the Earth either to exterminate and supplant human life, enslave it under an intense state, harvest people for food, steal the planet's resources, or destroy the planet altogether. ", price="$7.50", author=" J.R.R. Tolkien", category=cat1)

session.add(catItem2)

catItem3 = CategoryItem(name="The Hitchhiker's Guide To The Galaxy", description="In the first, hilarious volume of Adams' Hitchhiker's series, reluctant galactic traveler Arthur Dent gets swept up in some literally Earth-shattering events involving aliens, sperm whales, a depressed robot, mice who are more than they seem, and some really, really bad poetry. ", price="$17.50", author=" Douglas Adams", category=cat1)

session.add(catItem3)

catItem4 = CategoryItem(name="Ender's Game", description="Young Andrew Ender Wiggin, bred to be a genius, is drafted to Battle School where he trains to lead the century-long fight against the alien Buggers.", price="$19.50", author=" Orson Scott Card", category=cat1)

session.add(catItem4)

catItem5 = CategoryItem(name="The Dune Chronicles", description="Young Andrew Ender Wiggin, bred to be a genius, is drafted to Battle School where he trains to lead the century-long fight against the alien Buggers.", price="$7.50", author=" Frank Herbert", category=cat1)

session.add(catItem5)

# Books for Category Children's book series

catItem6 = CategoryItem(name="The Secrets of Droon", description="The Secrets of Droon is a fantasy book series by Tony Abbott aimed at elementary school-age children. The first book, The Hidden Stairs and the Magic Carpet, was published on June 1, 1999. On October 1, 2010, the final book of the series.", price="$7.50", author="Tony Abbott", category=cat2)

session.add(catItem6)

catItem7 = CategoryItem(name="Sam Hawkins, Pirate Detective", description="TSam Hawkins, Pirate Detective is a series of comedy children's books by Ian Billings. The first book, Sam Hawkins Pirate Detective and the Case of the Cutglass Cutlass was published by Macmillan Publishers in 2003. The sequel, Sam Hawkins Pirate Detective and the Pointy Head Lighthouse was published in 2004.", price="$12.50", author="Ian Billings", category=cat2)

session.add(catItem7)

catItem8 = CategoryItem(name="The Famous Five", description="The Famous Five is a series of children's adventure novels written by English author Enid Blyton. The first book, Five on a Treasure Island, was published in 1942. The novels feature the adventures of a group of young children – Julian, Dick, Anne and Georgina (George) – and their dog Timmy.", price="$22.50", author="Enid Blyton", category=cat2, best_seller_rank=2)

session.add(catItem8)

catItem9 = CategoryItem(name="Nancy Drew Mystery Stories", description="The Nancy Drew Mystery Stories is the long-running main Nancy Drew series, which was published under the pseudonym Carolyn Keene. There are 175 novels — plus 34 revised stories — that were published between 1930 and 2003 under the banner; Grosset & Dunlap published the first 56, and 34 revised stories, while Simon & Schuster published the series beginning with volume 57.", price="$22.50", author="Carolyn Keene", category=cat2, best_seller_rank=1)

session.add(catItem9)

catItem10 = CategoryItem(name="The Chronicles of Narnia", description="The Chronicles of Narnia is a series of seven fantasy novels by C. S. Lewis. It is considered a classic of children's literature and is the author's best-known work, having sold over 100 million copies in 47 languages.[1][2] Written by Lewis, illustrated by Pauline Baynes, and originally published in London between 1950 and 1956, The Chronicles of Narnia has been adapted several times, complete or in part, for radio, television, the stage, and film.", price="$67.50", author="C.S. Lewis", category=cat2, best_seller_rank=1)

session.add(catItem10)

# Books for Meditation

catItem11 = CategoryItem(name="Practicing Mindfulness", description="From finding your breath to feeling grounded, these practice-based exercises make integrating mindfulness into your routine easy. With over 75 essential meditations―that take between 5-20 minutes from start to finish―Practicing Mindfulness is an approachable way to apply mindfulness in your day-to-day life.", price="$34.50", author="Matthew Sockolov", category=cat3, best_seller_rank=0)

session.add(catItem11)

catItem12 = CategoryItem(name="A Better Human", description="Of all the religions, creeds, and self-help manifestos the world has produced, most concentrate on how to achieve salvation in aspects other than the here-and-now, with our lives merely transitory testing grounds for a higher realm or our actions guided so that we maximize life in a state of 'enlightened hedonism,' consuming rapaciously but really achieving not much at all.", price="$2.50", author="George J. Bradley", category=cat3, best_seller_rank=0)

session.add(catItem12)

catItem13 = CategoryItem(name="The Essence of Self-Realization", description="Yogananda was one of the most significant spiritual teachers of the 20th century. Since his classic, Autobiography of a Yogi, was first published in 1946, its popularity has increased steadily throughout the world. The Essence of Self-Realization is filled with lessons and stories that Yogananda shared only with his closest disciples, this volume offers one of the most insightful and engaging glimpses into the life and lessons of a great sage. Much of the material presented here is not available anywhere else.", price="$9.50", author="Paramhansa Yogananda", category=cat3, best_seller_rank=0)

session.add(catItem13)

catItem14 = CategoryItem(name="Dear Universe", description="For years it has been said, “you can achieve anything you set your mind to.” But have you ever wondered why so many people struggle to achieve health, wealth, and happiness? Why do we bottle-up our emotions and feel like life is happening to us, rather than for us? Finally, Dear Universe reveals the real answers to create abundance, love, freedom, and joy in all areas of your life. From the moment you open it’s pages, you’ll begin to understand your hidden, untapped power to guide your emotions and create the life you want, no matter what you’re experiencing.", price="$20.50", author="Paramhansa Yogananda", category=cat3, best_seller_rank=0)

session.add(catItem14)

catItem15 = CategoryItem(name="Chakras: The Mystical Rainbow in You", description="Just like the body has nerve plexuses which bundle together hundreds of nerves in order to distribute them to various regions of the body, so too does the body have energy plexuses, also known as chakras, which allow one to “step down” energy from the higher realms into the physical body.There are seven main chakras in the body situated along the spine, as well as several “outside” the body which connect a person to the earth and to higher dimensional planes, including universal awareness. ", price="$20.50", author="Basmati", category=cat3, best_seller_rank=0)

session.add(catItem15)

# books for mythology

catItem16 = CategoryItem(name="Mythology: Timeless Tales of Gods and Heroes", description="Edith Hamilton's mythology succeeds like no other book in bringing to life for the modern reader the Greek, Roman and Norse myths that are the keystone of Western culture-the stories of gods and heroes that have inspired human creativity from antiquity to the present. ", price="$20.50", author="Edith Hamilton", category=cat4, best_seller_rank=0)

session.add(catItem16)

catItem17 = CategoryItem(name="Egyptian Mythology", description="From stories of resurrected mummies and thousand-year-old curses to powerful pharaohs and the coveted treasures of the Great Pyramids, ancient Egypt has had an unfaltering grip on the modern imagination. Now, in Egyptian Mythology, Geraldine Pinch offers a comprehensive introduction that untangles the mystery of Egyptian Myth.", price="$20.50", author="Geraldine Pinch", category=cat4, best_seller_rank=0)

session.add(catItem17)

catItem18 = CategoryItem(name="Norse Mythology ", description="In Norse Mythology, Gaiman stays true to the myths in envisioning the major Norse pantheon: Odin, the highest of the high, wise, daring, and cunning; Thor, Odin’s son, incredibly strong yet not the wisest of gods; and Loki―son of a giant―blood brother to Odin and a trickster and unsurpassable manipulator.", price="$89.50", author="Neil Gaiman", category=cat4, best_seller_rank=0)

session.add(catItem18)

catItem19 = CategoryItem(name="Norse Mythology ", description="In Norse Mythology, Gaiman stays true to the myths in envisioning the major Norse pantheon: Odin, the highest of the high, wise, daring, and cunning; Thor, Odin’s son, incredibly strong yet not the wisest of gods; and Loki―son of a giant―blood brother to Odin and a trickster and unsurpassable manipulator.", price="$89.50", author="Neil Gaiman", category=cat4, best_seller_rank=0)

session.add(catItem18)

# Books for Wisdom

catItem20 = CategoryItem(name="Seeking Wisdom: From Darwin to Munger", description="Peter Bevelin begins his fascinating book with Confucius' great wisdom: A man who has committed a mistake and doesn't correct it, is committing another mistake. Seeking Wisdom is the result of Bevelin's learning about attaining wisdom. His quest for wisdom originated partly from making mistakes himself and observing those of others but also from the philosophy of super-investor and Berkshire Hathaway Vice Chairman Charles Munger. ", price="$10.50", author="Peter Bevelin", category=cat5, best_seller_rank=0)

session.add(catItem20)

catItem20 = CategoryItem(name="The Wisdom of the Enneagram", description="The ancient symbol of the Enneagram has become one of today's most popular systems for self-understanding, based on nine distinct personality types. Now, two of the world's foremost Enneagram authorities introduce a powerful new way to use the Enneagram as a tool for personal transformation and development. ", price="$12.50", author="Prince Mark", category=cat5, best_seller_rank=0)

session.add(catItem20)

# Ancient History

catItem21 = CategoryItem(name="The History of the Ancient World", description="This is the first volume in a bold new series that tells the stories of all peoples, connecting historical events from Europe to the Middle East to the far coast of China, while still giving weight to the characteristics of each country. Susan Wise Bauer provides both sweeping scope and vivid attention to the individual lives that give flesh to abstract assertions about human history. This narrative history employs the methods of history from beneath - literature, epic traditions, private letters, and accounts - to connect kings and leaders with the lives of those they ruled. The result is an engrossing tapestry of human behavior from which we may draw conclusions about the direction of world events and the causes behind them. ", price="$35.50", author=" Susan Wise Bauer", category=cat6, best_seller_rank=0)

session.add(catItem21)

session.commit()

print("added Book categories and items!")