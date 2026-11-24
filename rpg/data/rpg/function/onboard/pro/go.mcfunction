# 只带这一名新人进序章（改自 rpg:prologue/start；忙的时候由 pro/try 排队）
tag @a remove rpg.pr.join
tag @s add rpg.pr.join
weather clear 1800s
execute in rpg:armageddon run forceload add -64 -64 63 63
scoreboard players set #state rpg_pr 1
scoreboard players set #t rpg_pr 0
scoreboard players set #next rpg_pr 0
scoreboard players set #built rpg_pr 0
scoreboard players set #bt rpg_pr 0
tellraw @a[tag=rpg.pr.join] {"text":"[序章] 正在准备战场…… Preparing the battlefield...","color":"#E8D9B0"}
