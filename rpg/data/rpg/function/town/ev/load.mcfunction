scoreboard objectives add rpg_te dummy
scoreboard objectives add rpg_te_seen dummy
bossbar add rpg:town_ev ""
bossbar set rpg:town_ev color yellow
bossbar set rpg:town_ev style notched_10
scoreboard players set #run rpg_te 0
schedule function rpg:town/ev/sec 20t
schedule function rpg:town/ev/quick 5t
scoreboard players set #2 rpg_te 2
scoreboard players set #3 rpg_te 3
scoreboard players set #12 rpg_te 12
scoreboard players set #30 rpg_te 30
scoreboard players set #50 rpg_te 50
