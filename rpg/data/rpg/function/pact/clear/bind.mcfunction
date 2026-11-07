# 这个人身上挣出来的领主记下他，阶位越高来的越强。
execute unless entity @s[tag=rpg.pact] run return 0
scoreboard players add #bid rpg_pact_bid 1
scoreboard players operation @s rpg_pact_bid = #bid rpg_pact_bid
scoreboard players operation #lv rpg_pact = @s rpg_pact_lv
execute as @e[type=minecraft:vindicator,tag=rpg.advent,distance=..4,sort=nearest,limit=1] unless score @s rpg_pact_bid matches 1.. run function rpg:pact/clear/bind_lord
