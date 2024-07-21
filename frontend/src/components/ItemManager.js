import React, { useState, useEffect } from 'react';
import ItemList from './ItemList';
import ItemForm from './ItemForm';
import axios from 'axios';

const ItemManager = () => {
  const [items, setItems] = useState([]);
  const [currentItem, setCurrentItem] = useState(null);
  //const backendApi = process.env.REACT_APP_BACKEND_API;
  const backendApi = process.env.REACT_APP_BACKEND_API || '/api';
  console.log(`backendApi list = ${backendApi}`)
  console.log(process.env)


  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await axios.get(`${backendApi}/items/`);
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const handleAddOrUpdate = async () => {
    await fetchItems(); // Refresh the item list after adding or updating
    setCurrentItem(null); // Clear the form
  };

  const handleEdit = (item) => {
    setCurrentItem(item);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${backendApi}/items/${id}`);
      await fetchItems(); // Refresh the item list after deleting
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  return (
    <div>
      <ItemForm currentItem={currentItem} onSave={handleAddOrUpdate} />
      <ItemList items={items} onEdit={handleEdit} onDelete={handleDelete} />
    </div>
  );
};

export default ItemManager;
