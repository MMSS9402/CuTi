import torch

def geodesic_loss(Ps, Gs, train_val='train'):
    """ Loss function for training network """

    ii, jj = torch.tensor([0, 1]), torch.tensor([1, 0]) 

    dP = Ps[:,jj] * Ps[:,ii].inv()
    #print("GS______",Gs)
    #print("GS[0]__ __ __ ", Gs[0])
    #print("GS[0][:,jj]",Gs[0][:,jj])
    dG = Gs[0][:,jj] * Gs[0][:,ii].inv()
    
    d = (dG * dP.inv()).log()
    #print("loss_d",d.data)

    tau, phi = d.split([3,3], dim=-1)
    #print("tau",tau.data)
    geodesic_loss_tr = tau.norm(dim=-1).mean()
    geodesic_loss_rot = phi.norm(dim=-1).mean()

    metrics = {
        train_val+'_geo_loss_tr': (geodesic_loss_tr).detach().item(),
        train_val+'_geo_loss_rot': (geodesic_loss_rot).detach().item(),
    }

    return geodesic_loss_tr, geodesic_loss_rot, metrics