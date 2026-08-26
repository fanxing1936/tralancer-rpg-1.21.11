tag @s add rpg.ch1.recap.anomaly
scoreboard players set @s rpg_ch1_time 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"+------ 案情复盘 · 异常 ------+","color":"#B8A98B","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"◆ 已知　","color":"#62D9E8","bold":true,"italic":false},{"text":"死者保留记忆外壳，处决日期却写在明天。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"◇ 矛盾　","color":"#FFF2A8","bold":true,"italic":false},{"text":"疫病解释不了预写命令，亡灵解释不了完整记忆。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"→ 下一步　","color":"#B5D957","bold":true,"italic":false},{"text":"找到钟灰指向的活见证人。","color":"gray","bold":false,"italic":false}]
