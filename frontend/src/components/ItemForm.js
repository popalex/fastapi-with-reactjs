import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ItemForm = ({ currentItem, onSave }) => {
  const backendApi = process.env.REACT_APP_BACKEND_API;
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    if (currentItem) {
      setName(currentItem.name);
      setDescription(currentItem.description);
    }
  }, [currentItem]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newItem = { name, description };

    try {
      if (currentItem) {
        await axios.put(`${backendApi}/items/${currentItem.id}`, newItem);
      } else {
        await axios.post(`${backendApi}/items/`, newItem);
      }
      onSave();
      setName('');
      setDescription('');
    } catch (error) {
      console.error('Error saving item:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{currentItem ? 'Edit Item' : 'Add Item'}</h2>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
        required
      />
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
        required
      />
      <button type="submit">{currentItem ? 'Update' : 'Add'}</button>
    </form>
  );
};

export default ItemForm;
