# 收场 5：清实体、放开区块
execute in rpg:daath positioned 2560.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 2528 -32 2592 32
bossbar set rpg:daath_5 players
bossbar set rpg:daath_5 visible false
scoreboard players set #b5 rpg_dt 0
data remove storage rpg:daath s5
