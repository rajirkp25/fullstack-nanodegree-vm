# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

from database_setup import Category, CategoryItem, User

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
# session = DBSession()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)

# Delete
db.session.query(User).delete()
db.session.query(Category).delete()
db.session.query(CategoryItem).delete()
db.session.commit()

# Categories
SoccerCat = Category(name='Soccer', description='Association football, more commonly known as football or soccer, nicknamed The World Game or The Beautiful Game, is a team sport played between two teams of eleven players with a spherical ball. It is played by 250 million players in over 200 countries and dependencies, making it the worlds most popular sport. The game is played on a rectangular field with a goal at each end. The object of the game is to score by getting the ball into the opposing goal.')
db.session.add(SoccerCat)
BasketballCat = Category(name='Basketball', description='Basketball is a sport, generally played by two teams of five players on a rectangular court. The objective is to shoot a ball through a hoop 18 inches (46 cm) in diameter and mounted at a height of 10 feet (3.048 m) to backboards at each end of the court.')
db.session.add(BasketballCat)
BaseballCat = Category(name='Baseball', description='Baseball is a bat-and-ball game played between two teams of nine players each, who take turns batting and fielding. The batting team attempts to score runs by hitting a ball that is thrown by the pitcher with a bat swung by the batter, then running counter-clockwise around a series of four bases: first, second, third, and home plate. A run is scored when a player advances around the bases and returns to home plate.')
db.session.add(BaseballCat)
FrisbeeCat = Category(name='Frisbee', description='A frisbee (sometimes called a flying disc) is a disc-shaped gliding toy or sporting item that is generally plastic and roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip,[1] used recreationally and competitively for throwing and catching, for example, in flying disc games. The shape of the disc, an airfoil in cross-section, allows it to fly by generating lift as it moves through the air while spinning.')
db.session.add(FrisbeeCat)
SnowboardingCat = Category(name='Snowboarding', description='Snowboarding is a recreational activity and Olympic and Paralympic sport that involves descending a snow-covered slope while standing on a snowboard attached to a riders feet. The development of snowboarding was inspired by skateboarding, sledding, surfing and skiing. It was developed in the United States in the 1960s, became a Winter Olympic Sport at Nagano in 1998[1] and first featured in the Winter Paralympics at Sochi in 2014.[2] Its popularity (as measured by equipment sales) in the United States peaked in 2007 and has been in a decline since.[3]')
db.session.add(SnowboardingCat)
RockClimbingCat = Category(name='Rock Climbing', description='Rock climbing is an activity in which participants climb up, down or across natural rock formations or artificial rock walls. The goal is to reach the summit of a formation or the endpoint of a usually pre-defined route without falling. Due to the length and extended endurance required and because accidents are more likely to happen on descent than ascent, Rock Climbers do not usually climb back down the route. It is very rare for a climber to downclimb, especially on the larger multiple pitches (class III- IV and /or multi-day grades IV-VI climbs). Professional Rock climbing competitions have the objectives of either completing the route in the quickest possible time or attaining the farthest point on an increasingly difficult route. Scrambling, another activity involving the scaling of hills and similar formations, is similar to rock climbing. However, rock climbing is generally differentiated by its sustained use of hands to support the climbers weight as well as to provide balance.')
db.session.add(RockClimbingCat)
FoosballCat = Category(name='Foosball', description='Table football, commonly called fuzboll or foosball (as in the German Fussball football) and sometimes table soccer, is a table-top game, sport, that is loosely based on association football.')
db.session.add(FoosballCat)
SkatingCat = Category(name='Skating', description='Ice skating is the act of moving on ice by using ice skates. It can be done for a variety of reasons, including exercise, leisure, traveling, and various sports. Ice skating occurs both on specially prepared ice surfaces (arenas, tracks, parks), both indoors and outdoors, as well as on naturally occurring bodies of frozen water, such as ponds, lakes and rivers.')
db.session.add(SkatingCat)
HockeyCat = Category(name='Hockey', description='Hockey is a family of sports in which two teams play against each other by trying to maneuver a ball or a puck into the opponents goal using a hockey stick. In many areas, one sport (typically field hockey or ice hockey[1]) is generally referred to simply as hockey.')
db.session.add(HockeyCat)
db.session.commit()

# Category Items
db.session.add(CategoryItem(name='Stick', category=SoccerCat, description="A hockey stick is a piece of equipment used in field hockey, ice hockey , roller hockey or underwater hockey to move the ball or puck."))
db.session.add(CategoryItem(name='Goggles', category=SnowboardingCat, description="Goggles or safety glasses are forms of protective eyewear that usually enclose or protect the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes. They are used in chemistry laboratories and in woodworking. They are often used in snow sports as well, and in swimming. Goggles are often worn when using power tools such as drills or chainsaws to prevent flying particles from damaging the eyes. Many types of goggles are available as prescription goggles for those with vision problems."))
db.session.add(CategoryItem(name='Snowboard', category=SnowboardingCat, description="Snowboards are boards that are usually the width of one's foot longways, with the ability to glide on snow.[1] Snowboards are differentiated from monoskis by the stance of the user. In monoskiing, the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the longitude of the board. Users of such equipment may be referred to as snowboarders. Commercial snowboards generally require extra equipment such as bindings and special boots which help secure both feet of a snowboarder, who generally rides in an upright position.[1] These types of boards are commonly used by people at ski hills or resorts for leisure, entertainment, and competitive purposes in the activity called snowboarding."))
db.session.add(CategoryItem(name='Shinguards', category=SoccerCat, description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury. These are commonly used in sports including association football (soccer), baseball, ice hockey, field hockey, lacrosse, rugby, cricket, and other sports. This is due to either being required by the rules/laws of the sport or worn voluntarily by the participants for protective measures."))
db.session.add(CategoryItem(name='Frisbee', category=FrisbeeCat, description="A frisbee (sometimes called a flying disc) is a disc-shaped gliding toy or sporting item that is generally plastic and roughly 20 to 25 centimetres (8 to 10 in) in diameter with a lip,[1] used recreationally and competitively for throwing and catching, for example, in flying disc games. The shape of the disc, an airfoil in cross-section, allows it to fly by generating lift as it moves through the air while spinning."))
db.session.add(CategoryItem(name='Bat', category=BaseballCat, description="A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches in diameter at the thickest part and no more than 42 inches (1,100 mm) long. Although historically bats approaching 3 pounds (1.4 kg) were swung,[1] today bats of 33 ounces (0.94 kg) are common, topping out at 34 ounces (0.96 kg) to 36 ounces (1.0 kg).[1]"))
db.session.add(CategoryItem(name='Kit', category=SoccerCat, description="In association football, kit (also referred to as strip or soccer uniform) is the standard equipment and attire worn by players. The sport's Laws of the Game specify the minimum kit which a player must use, and also prohibit the use of anything that is dangerous to either the player or another participant. Individual competitions may stipulate further restrictions, such as regulating the size of logos displayed on shirts and stating that, in the event of a match between teams with identical or similar colours, the away team must change to different coloured attire."))
db.session.add(CategoryItem(name='Cleats', category=SoccerCat, description="Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface. In American English the term cleats is used synecdochically to refer to shoes featuring such protrusions. This does not happen in British English; the term 'studs' is never used to refer to the shoes, which would instead be known as 'football boots', 'rugby boots', and so on."))
db.session.commit()

print ("added catalog items!")





