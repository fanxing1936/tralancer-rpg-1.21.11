# 收场 13：清实体、放开区块
execute in rpg:daath positioned 6656.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 6624 -32 6688 32
bossbar set rpg:daath_13 players
bossbar set rpg:daath_13 visible false
scoreboard players set #b13 rpg_dt 0
data remove storage rpg:daath s13
