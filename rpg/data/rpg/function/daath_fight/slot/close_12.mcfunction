# 收场 12：清实体、放开区块
execute in rpg:daath positioned 6144.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 6112 -32 6176 32
bossbar set rpg:daath_12 players
bossbar set rpg:daath_12 visible false
scoreboard players set #b12 rpg_dt 0
data remove storage rpg:daath s12
