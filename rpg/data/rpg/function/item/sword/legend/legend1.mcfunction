# 更新前旧武器的统一入口。实际无持有者时内部立即跳过。
function rpg:item/legacy/weapons

##恶魔词缀
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g0


scoreboard players reset * devil_weapon

##天使词缀
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g1


scoreboard players reset * holy


##别西卜（现代入口）
# 余烬改为 30 刻蓄力与无实体刀罡；旧命名载体已退役。

##贝利尔（现代入口）
# 朝拜由独立 cast 函数处理，不再全局重置 blil。

##链锯（现代入口）
# 血痂已移入 rpg:item/legacy/weapons；不再使用 chainsaw/random 的全局 reset。

##漆黑之日（现代入口）
# 漆黑之刃改为 30 刻蓄力与一次定向斩击；旧每目标 TNT 循环已退役。

##高山（现代入口）
# 怒嚎已移入 rpg:item/legacy/weapons。

##风骨（现代入口）
# 黑白二式已移入 rpg:item/legacy/weapons，式样状态按玩家保存。

##剧毒之牙（现代入口）
# 淬毒已移入 rpg:item/legacy/weapons，毒层按攻击者保存。


##无垠星空／樱怒之日／漆黑之日（现代命中入口）
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/saber_victim
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/sakura_victim
# 兼容清理旧存档中没有可追溯主人的樱花箭；新版不再生成它们。
execute if entity @e[type=minecraft:spectral_arrow,tag=sakura_tag] run function rpg:item/legacy_advanced/sakura_cleanup

##亚巴顿（现代入口）
# 收割并入精确命中入口，不再让伤害递归写回 soul 统计。

##风之回响（现代入口）
# 狂风改为 30 刻蓄力与三道无实体风路；旧命名载体已退役。


##如意金箍棒（现代命中入口）
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/wukong_victim

##朗基努斯（现代入口）
# 王座标记与处决均按玩家归属；旧最近玩家定向已退役。

##史诗武器（六件随机属性精英武器的共同运行时）
# 属性随机仍由 rpg:trial/epic_sword 保留；这里只处理技能归属。
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/epic_victim
function rpg:item/legacy_advanced/epic/tick

##教条战斧（现代命中入口）
execute as @e[tag=rpg.hurt] at @s run function rpg:item/legacy_advanced/hit/axe_victim
