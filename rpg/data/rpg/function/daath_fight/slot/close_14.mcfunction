# 收场 14：清实体、放开区块
execute in rpg:daath positioned 7168.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 7136 -32 7200 32
bossbar set rpg:daath_14 players
bossbar set rpg:daath_14 visible false
scoreboard players set #b14 rpg_dt 0
data remove storage rpg:daath s14
