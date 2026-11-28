scoreboard objectives add rpg_tw dummy
scoreboard objectives add rpg_tw_id dummy
scoreboard objectives add rpg_tw_home dummy
scoreboard objectives add rpg_tw_at dummy
scoreboard objectives add rpg_tw_wait dummy
scoreboard objectives add rpg_tw_gm dummy
scoreboard objectives add rpg_tw_ev dummy
execute unless score #init rpg_tw matches 1 run function rpg:town/init
execute unless score #campv rpg_tw matches 1 run function rpg:town/job/campfix
scoreboard players set #cur rpg_tw 0
scoreboard players set #2 rpg_tw 2
schedule function rpg:town/job/tick 40t
schedule function rpg:town/sec 20t
