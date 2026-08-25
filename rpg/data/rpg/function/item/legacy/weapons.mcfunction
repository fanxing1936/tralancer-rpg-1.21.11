# 更新前旧武器的统一热路径。
# 这些旧武器都无人持有时不扫描 rpg.hurt；有命中时只扫一遍，再由 on attacker
# 精确找出攻击者。冷却、黑白式、毒层全部是玩家自己的分数。
scoreboard players add @a rpg_leg_cd 0
scoreboard players add @a rpg_pen_mode 0
scoreboard players add @a rpg_venom 0
execute as @a[scores={rpg_leg_cd=1..}] run scoreboard players remove @s rpg_leg_cd 1

# 为需要跨刻保存目标的王座印分配稳定玩家号。每名新玩家独立进入函数，
# 所以不会出现同一刻加入的玩家拿到相同编号。
execute as @a unless score @s rpg_legacy_uid matches 1.. run function rpg:item/legacy/assign_uid

# 四个老主动技现在与沉锚/熔流用同一种 hold 状态机：trigger 每刻把
# hold 顶回 3，松手后三刻清空未满蓄力。贝利尔是瞬发，单独只走冷却。
scoreboard players add @a rpg_night_hold 0
scoreboard players add @a rpg_ashes_hold 0
scoreboard players add @a rpg_wind_hold 0
scoreboard players add @a rpg_throne_hold 0
execute as @a[scores={rpg_night_hold=1..}] run scoreboard players remove @s rpg_night_hold 1
execute as @a[scores={rpg_ashes_hold=1..}] run scoreboard players remove @s rpg_ashes_hold 1
execute as @a[scores={rpg_wind_hold=1..}] run scoreboard players remove @s rpg_wind_hold 1
execute as @a[scores={rpg_throne_hold=1..}] run scoreboard players remove @s rpg_throne_hold 1
scoreboard players set @a[scores={rpg_night_hold=..0,rpg_night_chg=1..}] rpg_night_chg 0
scoreboard players set @a[scores={rpg_ashes_hold=..0,rpg_ashes_chg=1..}] rpg_ashes_chg 0
scoreboard players set @a[scores={rpg_wind_hold=..0,rpg_wind_chg=1..}] rpg_wind_chg 0
scoreboard players set @a[scores={rpg_throne_hold=..0,rpg_throne_chg=1..}] rpg_throne_chg 0
scoreboard players add @a rpg_blil_cd 0
execute as @a[scores={rpg_blil_cd=1..}] run scoreboard players remove @s rpg_blil_cd 1

# 王座标记有自己的寿命；目标死亡、卸载或到时都不会留下活动实体。
execute as @e[tag=rpg.throne.mark,scores={rpg_throne_mark=1..}] run scoreboard players remove @s rpg_throne_mark 1
tag @e[tag=rpg.throne.mark,scores={rpg_throne_mark=..0}] remove rpg.throne.mark

execute if entity @a[tag=rpg.h.chainsaw_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] if entity @a[tag=rpg.h.montain_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] if entity @a[tag=rpg.h.pen_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] if entity @a[tag=rpg.h.potion_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] unless entity @a[tag=rpg.h.potion_tag1] if entity @a[tag=rpg.h.soul_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] unless entity @a[tag=rpg.h.potion_tag1] unless entity @a[tag=rpg.h.soul_tag1] if entity @a[tag=rpg.h.ashes_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
execute unless entity @a[tag=rpg.h.chainsaw_tag1] unless entity @a[tag=rpg.h.montain_tag1] unless entity @a[tag=rpg.h.pen_tag1] unless entity @a[tag=rpg.h.potion_tag1] unless entity @a[tag=rpg.h.soul_tag1] unless entity @a[tag=rpg.h.ashes_tag1] if entity @a[tag=rpg.h.power_tag1] if entity @e[tag=rpg.hurt,limit=1] as @e[tag=rpg.hurt] at @s run function rpg:item/legacy/hit
