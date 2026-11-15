# 一名圣卫（at 落点，塔卫、重盾、术士随机一种，add_holy_guards.py），打上本场标签。
function rpg:holy_guard/summon
tag @e[type=minecraft:vindicator,tag=rpg.hg,tag=!rpg.pf.unit,distance=..2] add rpg.pf.unit
