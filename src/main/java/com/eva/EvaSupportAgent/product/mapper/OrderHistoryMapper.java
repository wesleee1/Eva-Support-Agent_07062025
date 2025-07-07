package com.eva.EvaSupportAgent.product.mapper;

import com.eva.EvaSupportAgent.product.model.OrderHistory;
import com.eva.EvaSupportAgent.product.vo.OrderHistoryVO;

public class OrderHistoryMapper {

    public static OrderHistory toEntity(OrderHistoryVO vo) {
        OrderHistory entity = new OrderHistory();
        entity.setId(vo.getId());
        entity.setUserId(vo.getUserId());
        entity.setProductId(vo.getProductId());
        entity.setQuantity(vo.getQuantity());
        entity.setPrice(vo.getPrice());
        entity.setStatus(vo.getStatus());
        entity.setProductName(vo.getProductName());
        entity.setOrderedOn(vo.getOrderedOn());
        return entity;
    }

    public static OrderHistoryVO toVO(OrderHistory entity) {
        OrderHistoryVO vo = new OrderHistoryVO();
        vo.setId(entity.getId());
        vo.setUserId(entity.getUserId());
        vo.setProductId(entity.getProductId());
        vo.setQuantity(entity.getQuantity());
        vo.setPrice(entity.getPrice());
        vo.setStatus(entity.getStatus());
        vo.setProductName(entity.getProductName());
        vo.setOrderedOn(entity.getOrderedOn());

        return vo;
    }
}
