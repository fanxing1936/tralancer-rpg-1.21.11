# 带罪者每次挨打都要多还一笔。15 刻的间隔避开无敌帧，也断了自伤触发自伤的循环。
scoreboard players set @s rpg_luci_cd 15
damage @s 4 minecraft:magic
particle dust_color_transition{from_color:14344834,to_color:4895350,scale:2} ~ ~1 ~ 0.35 0.45 0.35 0.05 20
particle minecraft:flash{color:14344834} ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.warden_ambient player @a[distance=..16] ~ ~ ~ 0.4 2
