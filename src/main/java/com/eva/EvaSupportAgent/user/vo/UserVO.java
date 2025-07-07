package com.eva.EvaSupportAgent.user.vo;

import com.eva.EvaSupportAgent.user.model.User;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@Data
@NoArgsConstructor
public class UserVO {

    private Long id;
    private String name;
    private String email;
    private String phone;
    private boolean active;
    
    public UserVO(User user) {
        this.id = user.getId();
        this.name = user.getName();
        this.email = user.getEmail();
        this.phone = user.getPhone();
        this.active = user.isActive();
    }
}
