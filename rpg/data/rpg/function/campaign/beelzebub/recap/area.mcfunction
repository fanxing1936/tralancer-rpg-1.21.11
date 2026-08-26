tag @s add rpg.ch1.recap.area
scoreboard players set @s rpg_ch1_time 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"+------ 案情复盘 · 三线 ------+","color":"#B8A98B","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"◆ 已知　","color":"#62D9E8","bold":true,"italic":false},{"text":"口粮、尸体与灭口路线都汇入第七粮仓。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"◇ 矛盾　","color":"#FFF2A8","bold":true,"italic":false},{"text":"满仓封条后没有粮食，旧记录早于卡西安接任。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"→ 下一步　","color":"#B5D957","bold":true,"italic":false},{"text":"进入粮仓，以检材建立真名假说。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"卡西安：","color":"#D4AF37","bold":true,"italic":false},{"text":"移交污染档案。我会记录你们曾协助教廷。","color":"#706B5E","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"卡西安：","color":"#D4AF37","bold":true,"italic":false},{"text":"拒绝移交，即视为记录错误。","color":"#706B5E","bold":false,"italic":false}]
