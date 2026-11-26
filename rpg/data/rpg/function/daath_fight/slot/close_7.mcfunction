# 收场 7：清实体、放开区块
execute in rpg:daath positioned 3584.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 3552 -32 3616 32
bossbar set rpg:daath_7 players
bossbar set rpg:daath_7 visible false
scoreboard players set #b7 rpg_dt 0
data remove storage rpg:daath s7
