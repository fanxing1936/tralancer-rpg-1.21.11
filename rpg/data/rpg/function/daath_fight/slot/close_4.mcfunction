# 收场 4：清实体、放开区块
execute in rpg:daath positioned 2048.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 2016 -32 2080 32
bossbar set rpg:daath_4 players
bossbar set rpg:daath_4 visible false
scoreboard players set #b4 rpg_dt 0
data remove storage rpg:daath s4
