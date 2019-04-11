#!/bin/bash
findMotifsGenome.pl diff_pd_caud_adpd_vs_ctrl_up.bed hg38 diff_pd_caud_adpd_vs_ctrl_up -bg background.idr.bed &
findMotifsGenome.pl diff_pd_caud_adpd_vs_ctrl_down.bed hg38 diff_pd_caud_adpd_vs_ctrl_down -bg background.idr.bed & 


