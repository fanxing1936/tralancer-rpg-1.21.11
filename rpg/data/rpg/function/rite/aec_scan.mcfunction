# 给新出现的药水云验明正身，只验一次。
#
# 之所以要打标记：仪式那边原本只判"附近有没有 area_effect_cloud"，
# 于是**任何**滞留药水都能点燃图腾 —— 一瓶滞留伤害药水也行。
# 按 custom_color 认水，认过就挂 rpg.aec.seen，不再重复验。
execute as @e[type=minecraft:area_effect_cloud,tag=!rpg.aec.seen] run function rpg:rite/aec
