# 装备养成：计分板、常数与名字表（每次 /reload 重写）
scoreboard objectives add rpg_fg dummy
scoreboard objectives add rpg_fg_lk dummy
scoreboard objectives add rpg_fg_op dummy
scoreboard objectives add rpg_fg_uid dummy
scoreboard objectives add rpg_fg_arg dummy
scoreboard objectives add rpg_fg_arg2 dummy
scoreboard objectives add rpg_fg_id dummy
scoreboard objectives add rpg_fg_en dummy
scoreboard objectives add rpg_fg_hit dummy
scoreboard objectives add rpg_fg_idle dummy
scoreboard objectives add rpg_fg_rw dummy
scoreboard objectives add rpg_fg_rs dummy
scoreboard objectives add rpg_fg_calm dummy
scoreboard objectives add rpg_fg_lb dummy
scoreboard objectives add rpg_fg_burn dummy
scoreboard objectives add rpg_fg_bt dummy
scoreboard objectives add rpg_fg_mark dummy
scoreboard objectives add rpg_fg_mt dummy
scoreboard objectives add rpg_fg_hv dummy
scoreboard objectives add rpg_fg_hs dummy
scoreboard objectives add rpg_fg_vid dummy
scoreboard objectives add rpg_fg_ec dummy
scoreboard objectives add rpg_fg_ea dummy
scoreboard objectives add rpg_fg_eo dummy
scoreboard objectives add rpg_fg_shd dummy
scoreboard objectives add rpg_fg_bl dummy
scoreboard objectives add rpg_fg_blh dummy
scoreboard objectives add rpg_fg_tn dummy
scoreboard objectives add rpg_fg_shot dummy
scoreboard objectives add rpg_fg_crit dummy
scoreboard objectives add rpg_fg_t dummy
scoreboard objectives add rpg_fg_clk dummy
scoreboard objectives add rpg_fg_mc dummy
scoreboard objectives add rpg_fg_kx dummy
scoreboard objectives add rpg_fg_do trigger
scoreboard objectives add rpg_fg_dd minecraft.custom:minecraft.damage_dealt
scoreboard objectives add rpg_fg_bow minecraft.used:minecraft.bow
scoreboard objectives add rpg_fg_xbow minecraft.used:minecraft.crossbow
scoreboard players set #2 rpg_fg 2
scoreboard players set #3 rpg_fg 3
scoreboard players set #4 rpg_fg 4
scoreboard players set #5 rpg_fg 5
scoreboard players set #10 rpg_fg 10
scoreboard players set #15 rpg_fg 15
scoreboard players set #20 rpg_fg 20
scoreboard players set #25 rpg_fg 25
scoreboard players set #40 rpg_fg 40
scoreboard players set #60 rpg_fg 60
scoreboard players set #100 rpg_fg 100
scoreboard players set #150 rpg_fg 150
scoreboard players set #1000 rpg_fg 1000
scoreboard players set #10000 rpg_fg 10000
scoreboard players set #q0 rpg_fg -1000
scoreboard players add #uid rpg_fg 0
scoreboard players add #pid rpg_fg 0
scoreboard players add #vid rpg_fg 0
data modify storage rpg:forge names set value {src:{none:'{"text":"—","color":"#797979","bold":false,"italic":false}',faith:'{"text":"[信念]","color":"#FF3300","bold":true,"italic":false}',hope:'{"text":"[希望]","color":"#FFF2A8","bold":true,"italic":false}',resolve:'{"text":"[不屈]","color":"#FFD85A","bold":true,"italic":false}',malice:'{"text":"[邪念]","color":"#D97AD9","bold":true,"italic":false}',hatred:'{"text":"[仇恨]","color":"#FF5C52","bold":true,"italic":false}',pride:'{"text":"[傲慢]","color":"#5FD68C","bold":true,"italic":false}'},srcd:{none:'{"text":"","color":"#FFFFFF","bold":false,"italic":false}',faith:'{"text":" 对亡灵与恶魔伤害 +25%","color":"gray","bold":false,"italic":false}',hope:'{"text":" 击杀回复 4 点生命并再生 3 秒","color":"gray","bold":false,"italic":false}',resolve:'{"text":" 受击后 3 秒内下一击 +30%","color":"gray","bold":false,"italic":false}',malice:'{"text":" 伤害 +15%","color":"gray","bold":false,"italic":false}',hatred:'{"text":" 连击同一目标每击 +5%，至多 +30%","color":"gray","bold":false,"italic":false}',pride:'{"text":" 满血时伤害 +30%","color":"gray","bold":false,"italic":false}'},rune:{none:'{"text":"—","color":"#797979","bold":false,"italic":false}',lock:'{"text":"🔒Lv.5","color":"#797979","bold":false,"italic":false}',ember:'{"text":"[余烬]","color":"#EC8A4C","bold":true,"italic":false}',echo:'{"text":"[回响]","color":"#EC8A4C","bold":true,"italic":false}',execute:'{"text":"[处决]","color":"#EC8A4C","bold":true,"italic":false}',backstab:'{"text":"[背刺]","color":"#EC8A4C","bold":true,"italic":false}',bloodpact:'{"text":"[血契]","color":"#EC8A4C","bold":true,"italic":false}',poise:'{"text":"[蓄势]","color":"#EC8A4C","bold":true,"italic":false}',hunt:'{"text":"[追猎]","color":"#93CC5C","bold":true,"italic":false}',split:'{"text":"[裂矢]","color":"#93CC5C","bold":true,"italic":false}',meteor:'{"text":"[坠星]","color":"#93CC5C","bold":true,"italic":false}',recoil:'{"text":"[反震]","color":"#58BCEC","bold":true,"italic":false}',lastbreath:'{"text":"[余生]","color":"#58BCEC","bold":true,"italic":false}',stillwater:'{"text":"[静水]","color":"#58BCEC","bold":true,"italic":false}',swift:'{"text":"[疾行]","color":"#58BCEC","bold":true,"italic":false}'},stone:{none:'{"text":"—","color":"#797979","bold":false,"italic":false}',na:'{"text":"不可镶嵌","color":"#797979","bold":false,"italic":false}',rift:'{"text":"[裂地]","color":"#DDA13F","bold":true,"italic":false}',frost:'{"text":"[寒潮]","color":"#62D9E8","bold":true,"italic":false}',shadow:'{"text":"[影步]","color":"#A276BE","bold":true,"italic":false}',blood:'{"text":"[血祭]","color":"#FF6B5E","bold":true,"italic":false}',gale:'{"text":"[风墙]","color":"#E8F4FF","bold":true,"italic":false}',volley:'{"text":"[箭雨]","color":"#70DB70","bold":true,"italic":false}',banner:'{"text":"[战旗]","color":"#FFD85A","bold":true,"italic":false}'}}
data modify storage rpg:forge bars set value ["▯▯▯▯▯","▮▯▯▯▯","▮▮▯▯▯","▮▮▮▯▯","▮▮▮▮▯","▮▮▮▮▮"]
data modify storage rpg:forge prefixes set value ["锐利的","千锤百炼的","坚固的","精制的","骑兵的","哨兵的","老兵的","无名的"]
