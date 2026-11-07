scoreboard players remove @s rpg_pf_l 1
execute if entity @s[tag=rpg.pf.blast] run function rpg:pope_fight/fx/blast
execute if entity @s[tag=rpg.pf.pillar] run function rpg:pope_fight/fx/pillar_tick
execute if entity @s[tag=rpg.pf.seal] run function rpg:pope_fight/fx/seal_tick
execute if entity @s[tag=rpg.pf.shard] run function rpg:pope_fight/fx/shard_tick
execute if entity @s[tag=rpg.pf.up] run tp @s ^ ^ ^1.3
execute if entity @s[tag=rpg.pf.fall] run function rpg:pope_fight/fx/fall
execute if entity @s[tag=rpg.pf.mark] run function rpg:pope_fight/fx/mark_tick
execute if entity @s[tag=rpg.pf.fill] run function rpg:pope_fight/fx/fill_tick
execute if entity @s[tag=rpg.pf.beam] run function rpg:pope_fight/fx/beam
execute if entity @s[tag=rpg.pf.flare] run function rpg:pope_fight/fx/flare_tick
execute if entity @s[tag=rpg.pf.puddle] run function rpg:pope_fight/fx/puddle_tick
execute if entity @s[tag=rpg.pf.pop] run function rpg:pope_fight/fx/pop_tick
execute if entity @s[tag=rpg.pf.halo] run function rpg:pope_fight/fx/halo_tick
execute if entity @s[tag=rpg.pf.chain] run function rpg:pope_fight/fx/chain_tick
execute if entity @s[tag=rpg.pf.flip] run function rpg:pope_fight/fx/flip_tick
execute if entity @s[tag=rpg.pf.vortex] run function rpg:pope_fight/fx/vortex_tick
execute if entity @s[tag=rpg.pf.charge] run function rpg:pope_fight/fx/charge_tick
execute if entity @s[tag=rpg.pf.judge] run function rpg:pope_fight/fx/judge_tick
execute if entity @s[tag=rpg.pf.nova] run function rpg:pope_fight/fx/nova_tick
execute if entity @s[tag=rpg.pf.vent] run function rpg:pope_fight/fx/vent_tick
execute if entity @s[tag=rpg.pf.more] run function rpg:pope_fight/fx/one_more
execute if score @s rpg_pf_l matches ..0 run kill @s
